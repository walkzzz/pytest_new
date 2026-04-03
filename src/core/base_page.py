from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class BasePage:
    def __init__(self, app, locators: Optional[Dict[str, Any]] = None):
        self.app = app
        self.locators = locators or {}

    def load_locators(self, locator_file: str) -> Dict[str, Any]:
        locator_path = Path("tests/locators") / locator_file
        if locator_path.exists():
            with open(locator_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def get_element(self, name: str, **kwargs):
        if name in self.locators:
            locators = self.locators[name].get("locators", {})
            locators.update(kwargs)
            return self.app.window(**locators)
        return None

    def wait_for_element(self, name: str, timeout: int = 10):
        elem = self.get_element(name)
        if elem:
            elem.wait_ready(timeout=timeout)
        return elem
