import atexit
import signal
import subprocess
import sys
from pathlib import Path

from factorio_state_exporter.install_mod import install_mod

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

    factorio_root = Path.home() / "Games" / "factorio"
    factorio_binary = factorio_root / "bin" / "x64" / "factorio"

    install_mod(factorio_root, port_num=33491, verbose=False)

    # Start factorio with UDP enabled
    factorio_proc = subprocess.Popen(
        [str(factorio_binary), "--enable-lua-udp", "6001"],
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
