import os
from string import Template
from typing import Any, Dict, Optional

import yaml


class YAMLLoader:
    @staticmethod
    def load(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_string(yaml_str: str) -> Dict[str, Any]:
        return yaml.safe_load(yaml_str)


class TemplateEngine:
    @staticmethod
    def render(value: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        context = context or {}
        if isinstance(value, str):
            return Template(value).safe_substitute(context)
        elif isinstance(value, dict):
            return {k: TemplateEngine.render(v, context) for k, v in value.items()}
        elif isinstance(value, list):
            return [TemplateEngine.render(item, context) for item in value]
        return value


def safe_load(stream):
    return yaml.safe_load(stream)


def dump(data, stream=None, **kwargs):
    return yaml.dump(data, stream, **kwargs)
