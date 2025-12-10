import tempfile
import unittest
from pathlib import Path

from factorio_state_exporter.install_mod import install_mod, mod_file_path


class TestModFilePath(unittest.TestCase):
    def test_mod_file_path_returns_valid_directory(self):
        """Test that mod_file_path returns a valid path to the mod directory."""
        path = Path(mod_file_path())
        self.assertTrue(path.exists())
        self.assertTrue(path.is_dir())
        self.assertTrue((path / "control.lua").exists())
        self.assertTrue((path / "info.json").exists())


class TestInstallMod(unittest.TestCase):
    def test_install_mod_copies_files_to_correct_location(self):
        """Test that install_mod copies mod files to mods/state-exporter."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "mods").mkdir()

            install_mod(tmp_path, port_num=12345, verbose=True)

            mod_dest = tmp_path / "mods" / "state-exporter"
            self.assertTrue(mod_dest.exists())
            self.assertTrue(mod_dest.is_dir())
            self.assertTrue((mod_dest / "info.json").exists())
            self.assertTrue((mod_dest / "control.lua").exists())

    def test_install_mod_generates_settings_lua_with_port_and_verbose(self):
        """Test that install_mod generates settings.lua with correct port and verbose values."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "mods").mkdir()

            install_mod(tmp_path, port_num=12345, verbose=True)

            settings_content = (tmp_path / "mods" / "state-exporter" / "settings.lua").read_text()
            self.assertIn("port_num = 12345", settings_content)
            self.assertIn("verbose = true", settings_content)

    def test_install_mod_generates_settings_lua_with_verbose_false(self):
        """Test that install_mod generates settings.lua with verbose=false when requested."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "mods").mkdir()

            install_mod(tmp_path, port_num=54321, verbose=False)

            settings_content = (tmp_path / "mods" / "state-exporter" / "settings.lua").read_text()
            self.assertIn("port_num = 54321", settings_content)
            self.assertIn("verbose = false", settings_content)


if __name__ == "__main__":
    unittest.main()
