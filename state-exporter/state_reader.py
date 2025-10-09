# Reads state_writer.lua's json game state into a dict.
# Also keeps track of when we've seen the last update.

import json
import socket
import threading
import time


class StateReader:
    def __init__(self, port):
        self.state = {}
        self.state_cv = threading.Condition()
        self.last_tick = 0
        self.port = port

    # Exposed for unit tests.
    def _update_state(self, state):
        with self.state_cv:
            self.state |= state
            self.last_tick = self.state.get("tick", 0)
            self.state_cv.notify_all()

    def _loop(self):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        localhost = "127.0.0.1"
        sock.bind((localhost, self.port))
        print(f"udp server up and listening on {localhost}:{self.port}")

        while True:
            message, address = sock.recvfrom(80_000)
            message = message.decode("utf-8")
            data = json.loads(message)
            self._update_state(data)

    def run(self):
        threading.Thread(target=self._loop, args=(), daemon=True).start()

    def get_state(self) -> dict[str, str | float]:
        with self.state_cv:
            return self.state.copy()

    def get_state_after_ticks(
        self, ticks, timeout_seconds=None
    ) -> dict[str, str | float] | None:
        with self.state_cv:
            start_tick = self.last_tick
            ok = self.state_cv.wait_for(
                lambda: self.last_tick >= start_tick + ticks,
                timeout_seconds,
            )
            return self.state.copy() if ok else None


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
