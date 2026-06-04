"""Launch the primer harness on a Lightning AI GPU Studio.

Runs from your laptop (no local GPU needed). It:
  1. authenticates with LIGHTNING_USER_ID / LIGHTNING_API_KEY (from .env),
  2. starts (or reuses) a Studio on a GPU,
  3. uploads the harness source,
  4. installs requirements and runs run.py (or sweep.py / scale_ladder.py),
  5. downloads results back here.

Usage:
    .venv/bin/python lightning_run.py            # five-arm test report on T4
    .venv/bin/python lightning_run.py --sweep    # val alpha x layer sweep
    .venv/bin/python lightning_run.py --ladder   # scale ladder across model sizes
    .venv/bin/python lightning_run.py --machine L4
    .venv/bin/python lightning_run.py --keep-running
    .venv/bin/python lightning_run.py --stop-only   # just stop the studio
"""
import argparse
import os
import pathlib
import time

# ---- load credentials from .env before importing the SDK -------------------
def _load_dotenv(path=".env"):
    p = pathlib.Path(path)
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_dotenv()

from lightning_sdk import Machine, Studio, Teamspace  # noqa: E402

USER = "4fortune8"
TEAMSPACE = "inference-optimization-project"
STUDIO_NAME = "primer-harness"
REMOTE_DIR = "primer-harness"  # relative to the studio home (~)

# The studio home directory is persistent storage that survives stop/start, so
# the HF cache lives there and the (slow) model download happens once. We pin
# HF_HOME to the default location so previously cached weights are reused. An
# authenticated HF_TOKEN avoids anonymous-rate-limit throttling on cold loads.
HF_CACHE = "$HOME/.cache/huggingface"


def _remote_env_prefix():
    """Shell prefix that points HF at the persistent cache (and token if set)."""
    parts = [
        f"export HF_HOME={HF_CACHE}",
        "export HF_HUB_ENABLE_HF_TRANSFER=0",
    ]
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if token:
        parts.append(f"export HF_TOKEN={token}")
        parts.append(f"export HUGGING_FACE_HUB_TOKEN={token}")
    return "; ".join(parts) + "; "

# Source files the harness needs (keep this list tight; no venv/.git/caches).
SOURCE_FILES = [
    "config.py", "model.py", "primers.py", "compress.py",
    "tasks.py", "suite.py", "metrics.py", "run.py", "sweep.py",
    "scale_ladder.py", "requirements.txt",
]


def get_studio(machine):
    ts = Teamspace(name=TEAMSPACE, user=USER)
    studio = Studio(name=STUDIO_NAME, teamspace=ts, user=USER, create_ok=True)
    status = studio.status.name.lower()
    if status == "running":
        if studio.machine != machine:
            print(f"Switching studio to {machine} ...")
            studio.switch_machine(machine)
    elif status in ("stopped", "notcreated", "not_created"):
        print(f"Starting studio '{STUDIO_NAME}' on {machine} ...")
        studio.start(machine)
    else:
        # Pending / starting (e.g. a previous launch is mid-provision). Don't
        # call start() again (that errors); just wait for it to come up.
        print(f"Studio is '{status}'; waiting for it to finish starting ...")
        for _ in range(120):  # up to ~10 min
            time.sleep(5)
            if studio.status.name.lower() == "running":
                break
        if studio.status.name.lower() != "running":
            raise SystemExit(f"Studio did not reach 'running' (still "
                             f"{studio.status.name}). Retry shortly.")
        if studio.machine != machine:
            print(f"Switching studio to {machine} ...")
            studio.switch_machine(machine)
    # Long, non-interactive model loads look "idle" to the platform; auto-sleep
    # (seen with auto_sleep_time=0) can reclaim the instance mid-run and break
    # the keepalive stream. Disable it for the duration of the batch run.
    try:
        studio.auto_sleep = False
        print("  auto-sleep disabled for this run")
    except Exception as e:
        print(f"  (could not disable auto-sleep: {e})")
    print(f"Studio status: {studio.status} | machine: {studio.machine}")
    return studio


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--machine", default="T4",
                    help="Lightning machine type (T4, L4, A10G, ...)")
    ap.add_argument("--keep-running", action="store_true",
                    help="leave the studio running after the run")
    ap.add_argument("--stop-only", action="store_true",
                    help="just stop the studio and exit")
    ap.add_argument("--sweep", action="store_true",
                    help="run sweep.py (alpha x layer on val) instead of run.py")
    ap.add_argument("--ladder", action="store_true",
                    help="run scale_ladder.py (identical harness across model sizes)")
    args = ap.parse_args()

    try:
        machine = getattr(Machine, args.machine)
    except AttributeError:
        avail = [m for m in dir(Machine) if m.isupper() and not m.startswith("_")]
        raise SystemExit(
            f"Unknown machine '{args.machine}'. Available: {', '.join(avail)}")

    if args.stop_only:
        ts = Teamspace(name=TEAMSPACE, user=USER)
        Studio(name=STUDIO_NAME, teamspace=ts, user=USER, create_ok=True).stop()
        print("Stopped.")
        return

    studio = get_studio(machine)
    env = _remote_env_prefix()
    if "HF_TOKEN" in env:
        print("  HF_TOKEN found locally -> passing to studio (authenticated downloads)")
    else:
        print("  no HF_TOKEN in env/.env -> anonymous HF downloads (may be throttled)")

    # 1) upload source
    studio.run(f"mkdir -p ~/{REMOTE_DIR}")
    studio.run(f"mkdir -p {HF_CACHE}")
    for fn in SOURCE_FILES:
        print(f"  uploading {fn}")
        studio.upload_file(fn, remote_path=f"{REMOTE_DIR}/{fn}")

    # The final test report (run.py) consumes the val-selected operating points
    # from sweep.json; ship it along if we have one locally.
    if not args.sweep and pathlib.Path("sweep.json").exists():
        print("  uploading sweep.json (val-selected operating points)")
        studio.upload_file("sweep.json", remote_path=f"{REMOTE_DIR}/sweep.json")

    # 2) install deps (first run is slow; torch is large)
    print("Installing requirements (first run downloads torch; be patient) ...")
    print(studio.run(
        f"{env}cd ~/{REMOTE_DIR} && pip install -q -r requirements.txt && echo DEPS_OK"))

    # 3) run the harness (full multi-domain test report, val sweep, or ladder)
    if args.ladder:
        script = "scale_ladder.py"
    elif args.sweep:
        script = "sweep.py"
    else:
        script = "run.py"
    print(f"Running {script} ...")
    out, code = studio.run_with_exit_code(f"{env}cd ~/{REMOTE_DIR} && python {script}")
    print(out)
    if code != 0:
        print(f"{script} exited with code {code}; not downloading results.")
        return

    # 4) pull results back to the laptop
    print("Downloading results ...")
    if args.ladder:
        downloads = [("ladder.json", "ladder.json"), ("ladder.png", "ladder.png")]
        # per-model result files have model-dependent names; list and fetch them.
        try:
            listing = studio.run(
                f"cd ~/{REMOTE_DIR} && ls results_*.json results_readable_*.md "
                f"sweep_*.json sweep_*.png 2>/dev/null")
            for fn in listing.split():
                fn = fn.strip()
                if fn:
                    downloads.append((fn, fn))
        except Exception as e:
            print(f"  (could not list per-model results: {e})")
    elif args.sweep:
        downloads = [("sweep.json", "sweep.json"), ("sweep.png", "sweep.png")]
    else:
        downloads = [("results.json", "results.json"),
                     ("results_readable.md", "results_readable.md")]
    for remote, local in downloads:
        try:
            studio.download_file(f"{REMOTE_DIR}/{remote}", local)
            print(f"  downloaded {local}")
        except Exception as e:
            print(f"  ({local} download skipped: {e})")
    try:
        studio.download_folder(f"{REMOTE_DIR}/primer_bank", "primer_bank")
    except Exception as e:  # bank is optional/cheap; don't fail the run over it
        print(f"(primer_bank download skipped: {e})")
    print("Done.")

    if not args.keep_running:
        print("Stopping studio to save GPU hours ...")
        studio.stop()


if __name__ == "__main__":
    main()
