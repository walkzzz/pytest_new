import os
from pathlib import Path


class Settings:
    BASE_DIR = Path(__file__).parent.parent.parent

    SCREENSHOT_DIR = BASE_DIR / "screenshots"
    ALLURE_REPORT_DIR = BASE_DIR / "allure-results"
    LOG_DIR = BASE_DIR / "logs"

    APP_PATH = os.getenv("APP_PATH", r"D:\Program Files\CBIM\modulelogin.exe")

    @classmethod
    def ensure_dirs(cls):
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        cls.ALLURE_REPORT_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)


Settings.ensure_dirs()
