# Reads state_writer.lua's json game state into a dict.
# Also keeps track of when we've seen the last update.

import json
import socket
import threading
import time


class StateReader:
    def __init__(self, port):
        self.state_lock = threading.Lock()
        self.state = {}
        self.port = port

    def _loop(self):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        ip = "127.0.0.1"
        sock.bind((ip, self.port))
        print(f"udp server up and listening on {ip}:{self.port}")

        while True:
            message, address = sock.recvfrom(80_000)
            message = message.decode("utf-8")

            data = json.loads(message)
            self.state_lock.acquire()
            self.state |= data
            self.state_lock.release()

    def run(self):
        t = threading.Thread(target=self._loop, args=(), daemon=True)
        t.start()

    def get_state(self) -> dict[str, str | float]:
        out = None
        self.state_lock.acquire()
        out = self.state.copy()
        self.state_lock.release()
        return out

    def get_state_after_ticks(self, ticks) -> dict[str, str | float]:
        # Wait for at least "ticks" number of ticks to have occurred.
        # Then return the current state.
        pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    else:
        port = 33491

    r = StateReader(port)
    r.run()
    while True:
        time.sleep(0.1)
        print("reader state: ", r.get_state())
