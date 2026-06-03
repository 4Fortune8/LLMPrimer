"""Launch the three-arm primer harness on a Lightning AI T4 Studio.

Runs from your laptop (no local GPU needed). It:
  1. authenticates with LIGHTNING_USER_ID / LIGHTNING_API_KEY (from .env),
  2. starts (or reuses) a Studio on a T4,
  3. uploads the harness source,
  4. installs requirements and runs `run.py`,
  5. downloads results.json (and the primer_bank) back here.

Usage:
    .venv/bin/python lightning_run.py            # run on T4, keep studio asleep after
    .venv/bin/python lightning_run.py --machine L4
    .venv/bin/python lightning_run.py --keep-running
    .venv/bin/python lightning_run.py --stop-only   # just stop the studio
"""
import argparse
import os
import pathlib

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

# Source files the harness needs (keep this list tight; no venv/.git/caches).
SOURCE_FILES = [
    "config.py", "model.py", "primers.py", "compress.py",
    "tasks.py", "metrics.py", "run.py", "requirements.txt",
]


def get_studio(machine):
    ts = Teamspace(name=TEAMSPACE, user=USER)
    studio = Studio(name=STUDIO_NAME, teamspace=ts, user=USER, create_ok=True)
    if studio.status.name.lower() != "running":
        print(f"Starting studio '{STUDIO_NAME}' on {machine} ...")
        studio.start(machine)
    elif studio.machine != machine:
        print(f"Switching studio to {machine} ...")
        studio.switch_machine(machine)
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
    args = ap.parse_args()

    machine = getattr(Machine, args.machine)

    if args.stop_only:
        ts = Teamspace(name=TEAMSPACE, user=USER)
        Studio(name=STUDIO_NAME, teamspace=ts, user=USER, create_ok=True).stop()
        print("Stopped.")
        return

    studio = get_studio(machine)

    # 1) upload source
    studio.run(f"mkdir -p ~/{REMOTE_DIR}")
    for fn in SOURCE_FILES:
        print(f"  uploading {fn}")
        studio.upload_file(fn, remote_path=f"{REMOTE_DIR}/{fn}")

    # 2) install deps (first run is slow; torch is large)
    print("Installing requirements (first run downloads torch; be patient) ...")
    print(studio.run(f"cd ~/{REMOTE_DIR} && pip install -q -r requirements.txt && echo DEPS_OK"))

    # 3) run the three-arm harness
    print("Running harness ...")
    out, code = studio.run_with_exit_code(f"cd ~/{REMOTE_DIR} && python run.py")
    print(out)
    if code != 0:
        print(f"run.py exited with code {code}; not downloading results.")
        return

    # 4) pull results back to the laptop
    print("Downloading results ...")
    studio.download_file(f"{REMOTE_DIR}/results.json", "results.json")
    try:
        studio.download_folder(f"{REMOTE_DIR}/primer_bank", "primer_bank")
    except Exception as e:  # bank is optional/cheap; don't fail the run over it
        print(f"(primer_bank download skipped: {e})")
    print("Wrote results.json locally.")

    if not args.keep_running:
        print("Stopping studio to save GPU hours ...")
        studio.stop()


if __name__ == "__main__":
    main()
