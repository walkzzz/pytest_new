import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(env: Optional[str] = None) -> Dict[str, Any]:
    env = env or os.getenv("TEST_ENV", "test")
    config_dir = Path("tests/configs")

    env_config_path = config_dir / env / "app_config.yaml"
    default_config_path = config_dir / "test" / "app_config.yaml"

    if env_config_path.exists():
        return load_yaml(str(env_config_path))
    elif default_config_path.exists():
        return load_yaml(str(default_config_path))

    return {}


def load_test_data(data_path: str) -> Dict[str, Any]:
    full_path = Path("data") / data_path
    if full_path.exists():
        return load_yaml(str(full_path))
    return {}


def resolve_env_var(value: str) -> str:
    if value.startswith("${ENV:") and value.endswith("}"):
        var_name = value[6:-1]
        return os.getenv(var_name, "")
    return value
