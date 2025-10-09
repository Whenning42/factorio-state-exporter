# Reads state_writer.lua's json game state into a dict.
# Also keeps track of when we've seen the last update.

import socket
import threading
import time
import json

class StateReader:
    def __init__(self, port):
        self.state = {}
        self.port = port

    def _loop(self):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        ip = "127.0.0.1"
        sock.bind((ip, self.port))
        print(f"udp server up and listening on {ip}:{self.port}")

        while True:
            message, address = sock.recvfrom(80_000)
            message = message.decode('utf-8')

            print(message)
            data = json.loads(message)
            self.state = data | self.state

            print(f"Current state: {self.state}")

    def run(self):
        t = threading.Thread(target=self._loop, args=(), daemon=True)
        t.start()

    def get_state(self) -> dict[str, str | float]:
        # Return the state, make sure we don't
        # race/tear with the _loop.
        pass

    def get_state_after_ticks(self, ticks) -> dict[str, str | float]:
        # Wait for at least "ticks" number of ticks to have occurred.
        # Then return the current state.
        pass

if __name__ == "__main__":
    r = StateReader(6002)
    r.run()
    while True:
        time.sleep(10)
