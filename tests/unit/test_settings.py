import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestSettings:
    def test_base_dir_is_path(self):
        from src.config.settings import Settings

        assert isinstance(Settings.BASE_DIR, Path)

    def test_screenshot_dir_under_base_dir(self):
        from src.config.settings import Settings

        assert Settings.SCREENSHOT_DIR.is_relative_to(Settings.BASE_DIR)

    def test_allure_report_dir_under_base_dir(self):
        from src.config.settings import Settings

        assert Settings.ALLURE_REPORT_DIR.is_relative_to(Settings.BASE_DIR)

    def test_log_dir_under_base_dir(self):
        from src.config.settings import Settings

        assert Settings.LOG_DIR.is_relative_to(Settings.BASE_DIR)

    def test_app_path_has_default(self):
        from src.config.settings import Settings

        assert Settings.APP_PATH is not None
        assert len(Settings.APP_PATH) > 0

    @patch.dict(os.environ, {"APP_PATH": "D:\\Test\\app.exe"})
    def test_app_path_from_env(self):
        import importlib

        import src.config.settings

        importlib.reload(src.config.settings)
        from src.config.settings import Settings

        assert "Test" in Settings.APP_PATH

    def test_ensure_dirs_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                __import__("src.config.settings", fromlist=["Settings"]).Settings,
                "BASE_DIR",
                Path(tmpdir),
            ):
                with patch.object(
                    __import__("src.config.settings", fromlist=["Settings"]).Settings,
                    "SCREENSHOT_DIR",
                    Path(tmpdir) / "screenshots",
                ):
                    with patch.object(
                        __import__("src.config.settings", fromlist=["Settings"]).Settings,
                        "ALLURE_REPORT_DIR",
                        Path(tmpdir) / "allure-results",
                    ):
                        with patch.object(
                            __import__("src.config.settings", fromlist=["Settings"]).Settings,
                            "LOG_DIR",
                            Path(tmpdir) / "logs",
                        ):
                            from src.config.settings import Settings

                            class TestSettings(Settings):
                                BASE_DIR = Path(tmpdir)
                                SCREENSHOTS_DIR = Path(tmpdir) / "screenshots"
                                ALLURE_REPORT_DIR = Path(tmpdir) / "allure-results"
                                LOG_DIR = Path(tmpdir) / "logs"

                            TestSettings.SCREENSHOT_DIR = Path(tmpdir) / "screenshots"
                            TestSettings.ALLURE_REPORT_DIR = Path(tmpdir) / "allure-results"
                            TestSettings.LOG_DIR = Path(tmpdir) / "logs"
                            TestSettings.ensure_dirs()
                            assert (Path(tmpdir) / "screenshots").exists()
                            assert (Path(tmpdir) / "allure-results").exists()
                            assert (Path(tmpdir) / "logs").exists()
