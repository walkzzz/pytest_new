from typing import Any, Callable, Dict

import pytest


@pytest.fixture(scope="session")
def app_config():
    return {
        "process_name": "modulelogin.exe",
        "backend": "uia",
        "app_path": "D:\\Program Files\\CBIM\\modulelogin.exe",
        "start_timeout": 10,
    }


@pytest.fixture
def data_factory() -> Callable[[str, Dict[str, Any]], Dict[str, Any]]:
    def _create_test_data(data_type: str, overrides: Dict[str, Any] = None) -> Dict[str, Any]:
        base_data = {
            "normal": {
                "avatar_filename": "avatar_海葵_128x128.png",
                "signature_filename": "marker.png",
                "nickname": "test",
                "password": "123456",
            },
            "invalid_nickname": {
                "avatar_filename": "avatar_海葵_128x128.png",
                "signature_filename": "marker.png",
                "nickname": "66",
                "password": "123456",
            },
            "invalid_password": {
                "avatar_filename": "avatar_海葵_128x128.png",
                "signature_filename": "marker.png",
                "nickname": "88",
                "password": "123456",
            },
        }

        data = base_data.get(data_type, base_data["normal"]).copy()
        if overrides:
            data.update(overrides)
        return data

    return _create_test_data
