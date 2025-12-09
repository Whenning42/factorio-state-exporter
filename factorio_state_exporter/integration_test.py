import atexit
import os
import signal
import subprocess
import sys
from pathlib import Path

processes = []


def cleanup():
    """Kill all child processes on exit."""
    for proc in processes:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


def signal_handler(signum, frame):
    """Handle termination signals."""
    cleanup()
    sys.exit(0)


if __name__ == "__main__":
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    factorio_path = Path.home() / "Games" / "factorio" / "bin" / "x64" / "factorio"

    # Start factorio with UDP enabled
    factorio_proc = subprocess.Popen(
        [str(factorio_path), "--enable-lua-udp", "6001"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    processes.append(factorio_proc)

    # Start state reader
    state_reader_proc = subprocess.Popen(
        [sys.executable, "factorio_state_exporter/state_reader.py"],
    )
    processes.append(state_reader_proc)

    # Wait for both processes
    try:
        factorio_proc.wait()
        state_reader_proc.wait()
    except KeyboardInterrupt:
        cleanup()
