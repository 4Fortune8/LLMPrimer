"""Attach-and-finish monitor for an already-running remote scale_ladder.py.

The local launcher lost its stream (backgrounded process got SIGHUP), but the
remote scale_ladder.py kept running on the studio. This script polls the studio,
prints progress, and once the remote process exits it downloads every artifact
(ladder.json/png, results_*, sweep_*) and stops the studio. Idempotent and safe
to re-run; it never starts a second run.
"""
import os
import time

from lightning_sdk import Studio, Teamspace

USER = "4fortune8"
TEAMSPACE = "inference-optimization-project"
STUDIO_NAME = "primer-harness"
REMOTE_DIR = "primer-harness"

DL = ["ladder.json", "ladder.png"]


def main():
    ts = Teamspace(name=TEAMSPACE, user=USER)
    s = Studio(name=STUDIO_NAME, teamspace=ts, user=USER, create_ok=True)
    print(f"status={s.status} machine={s.machine}", flush=True)

    while True:
        out = s.run(
            f"cd ~/{REMOTE_DIR} && setopt null_glob 2>/dev/null; "
            f"(pgrep -f 'python scale_ladder' >/dev/null && echo RUNNING || echo DONE); "
            f"echo ---FILES---; ls -1 results_*.json sweep_*.json ladder.json 2>/dev/null; "
            f"echo ---PROGRESS---")
        print(time.strftime("%H:%M:%S"), out[:1500], flush=True)
        if "DONE" in out.split("---FILES---")[0]:
            print("Remote scale_ladder.py has exited.", flush=True)
            break
        time.sleep(60)

    # Discover every artifact and download it.
    listing = s.run(
        f"cd ~/{REMOTE_DIR} && setopt null_glob 2>/dev/null; ls -1 results_*.json "
        f"results_readable_*.md sweep_*.json sweep_*.png ladder.json ladder.png 2>/dev/null")
    files = sorted({f.strip() for f in listing.split() if f.strip()})
    print("Downloading:", files, flush=True)
    for fn in files:
        try:
            s.download_file(f"{REMOTE_DIR}/{fn}", fn)
            print("  got", fn, flush=True)
        except Exception as e:
            print(f"  !! failed {fn}: {e}", flush=True)

    print("Stopping studio ...", flush=True)
    try:
        s.stop()
        print("Stopped.", flush=True)
    except Exception as e:
        print(f"  (could not stop: {e})", flush=True)


if __name__ == "__main__":
    main()
