import threading
import time
import unittest
from pathlib import Path

from state_reader import StateReader, mod_file_path


class TestStateReader(unittest.TestCase):
    def test_get_state(self):
        """Test that get_state returns the state set by _update_state."""
        reader = StateReader(port=12345)
        test_state = {"test": "dict"}
        reader._update_state(test_state)
        self.assertEqual(reader.get_state(), test_state)

    def test_get_state_after_ticks_succeeds(self):
        """Test that get_state_after_ticks waits for the correct tick count."""
        reader = StateReader(port=12345)
        reader._update_state({"tick": 5})

        test_exit = False

        def update_state():
            for n in range(5, 11):
                if test_exit:
                    break
                reader._update_state({"tick": n, "data": f"at_{n}"})
                time.sleep(0.1)

        thread = threading.Thread(target=update_state)
        thread.start()

        result = reader.get_state_after_ticks(ticks=3, timeout_seconds=2)
        test_exit = True
        thread.join()

        self.assertEqual(result, {"tick": 8, "data": "at_8"})

    def test_get_state_after_ticks_timeout_returns_none(self):
        """Test that get_state_after_ticks returns None on timeout."""
        reader = StateReader(port=12345)

        reader._update_state({"tick": 3})
        result = reader.get_state_after_ticks(ticks=1, timeout_seconds=0.2)

        self.assertIsNone(result)

    def test_mod_file_path(self):
        """Test that mod_file_path returns a valid path to the mod directory."""
        path = Path(mod_file_path())
        self.assertTrue(path.exists(), f"mod directory does not exist at {path}")
        self.assertTrue(path.is_dir(), f"{path} is not a directory")
        self.assertTrue(
            (path / "control.lua").exists(), "control.lua not found in mod directory"
        )
        self.assertTrue(
            (path / "info.json").exists(), "info.json not found in mod directory"
        )


if __name__ == "__main__":
    unittest.main()
