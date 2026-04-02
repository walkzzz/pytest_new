import os
import yaml
from typing import Any, Dict, List, Optional, Tuple

from src.config.constants import (
    TEMPLATE_PATH,
    SUPPORTED_CONTROL_TYPES,
    SUPPORTED_EXECUTOR_METHODS,
    SUPPORTED_ASSERTION_METHODS,
)
from src.config.yaml_loader import YAMLLoader, TemplateEngine


class Config:
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        return YAMLLoader.load(config_path)

    @staticmethod
    def get_config(config_path: str, section: Optional[str] = None) -> Dict[str, Any]:
        config = Config.load_config(config_path)
        if section:
            if section not in config:
                raise KeyError(f"配置节不存在: {section}")
            return config[section]
        return config

    @staticmethod
    def resolve_template(template: str, context: Dict[str, Any]) -> str:
        return TemplateEngine.render(template, context)

    @staticmethod
    def get_app_config(config: Dict[str, Any]) -> Dict[str, Any]:
        return config.get("app", {})

    @staticmethod
    def get_controls_config(config: Dict[str, Any]) -> Dict[str, Any]:
        return config.get("controls", {})

    @staticmethod
    def get_test_data(config: Dict[str, Any]) -> Dict[str, Any]:
        return config.get("test_data", {})

    @staticmethod
    def get_test_cases(config: Dict[str, Any]) -> Dict[str, Any]:
        return config.get("test_cases", {})

    @staticmethod
    def get_timeouts(config: Dict[str, Any]) -> Dict[str, float]:
        return config.get("timeouts", {"short": 0.2, "normal": 0.5, "long": 1.0})

    @staticmethod
    def get_test_case(config: Dict[str, Any], test_case_name: str) -> Dict[str, Any]:
        test_cases = Config.get_test_cases(config)
        if test_case_name not in test_cases:
            raise KeyError(f"测试用例不存在: {test_case_name}")
        return test_cases[test_case_name]

    @staticmethod
    def get_test_case_data(
        config: Dict[str, Any], test_case: Dict[str, Any]
    ) -> Dict[str, Any]:
        test_data_name = test_case.get("test_data")
        if not test_data_name:
            return {}
        all_test_data = Config.get_test_data(config)
        return all_test_data.get(test_data_name, {})

    @staticmethod
    def get_test_case_steps(test_case: Dict[str, Any]) -> List[Dict[str, Any]]:
        return test_case.get("steps", [])

    @staticmethod
    def parse_test_case(config: Dict[str, Any], test_case_name: str) -> Dict[str, Any]:
        test_case = Config.get_test_case(config, test_case_name)
        test_data = Config.get_test_case_data(config, test_case)
        steps = Config.get_test_case_steps(test_case)

        # 解析步骤中的模板变量
        resolved_steps = Config._resolve_steps_template(steps, test_data)

        return {
            "name": test_case_name,
            "description": test_case.get("description", ""),
            "test_data": test_data,
            "steps": resolved_steps,
        }

    @staticmethod
    def _resolve_steps_template(steps: List[Dict], test_data: Dict) -> List[Dict]:
        """解析步骤中的模板变量 {{test_data.xxx}}"""
        import re

        def replace_template(value):
            if isinstance(value, str):
                pattern = r"\{\{test_data\.(\w+)\}\}"
                matches = re.findall(pattern, value)
                for match in matches:
                    if match in test_data:
                        value = value.replace(
                            f"{{{{test_data.{match}}}}}", str(test_data[match])
                        )
                return value
            elif isinstance(value, dict):
                return {k: replace_template(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_template(item) for item in value]
            return value

        return [replace_template(step) for step in steps]

    @staticmethod
    def get_template_config() -> Dict[str, Any]:
        return Config.load_config(TEMPLATE_PATH)

    @staticmethod
    def generate_template() -> Dict[str, Any]:
        return {
            "app": {
                "process_name": "应用进程名.exe",
                "backend": "uia",
                "main_window": {"title": "主窗口标题", "state": "visible"},
            },
            "controls": {
                f"{ctrl_type}_example": {
                    "type": ctrl_type,
                    "locator": {"title": f"{ctrl_type}标题"},
                }
                for ctrl_type in SUPPORTED_CONTROL_TYPES
            },
            "test_data": {"test_case_1": {"field1": "值1", "field2": "值2"}},
            "test_cases": {
                "test_case_1": {
                    "description": "测试用例描述",
                    "test_data": "test_case_1",
                    "steps": [
                        {
                            "name": "step-001: 步骤名称",
                            "action": {
                                "control": "button_example",
                                "method": "click",
                                "params": [],
                            },
                            "assertions": [
                                {
                                    "control": "button_example",
                                    "checks": ["visible", "enabled"],
                                }
                            ],
                            "timeout": "normal",
                        }
                    ],
                }
            },
            "timeouts": {"short": 0.2, "normal": 0.5, "long": 1.0},
        }

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> List[str]:
        errors = []
        if "app" not in config:
            errors.append("缺少 'app' 配置节")
        if "controls" not in config:
            errors.append("缺少 'controls' 配置节")
        if "test_cases" not in config:
            errors.append("缺少 'test_cases' 配置节")
        return errors

    @staticmethod
    def get_control_locator(
        controls_config: Dict[str, Any], control_name: str
    ) -> Tuple[str, Dict[str, Any]]:
        if control_name not in controls_config:
            raise KeyError(f"控件不存在: {control_name}")
        control_config = controls_config[control_name]
        control_type = control_config.get("type", "base")
        locator = control_config.get("locator", {})
        return control_type, locator

    @staticmethod
    def get_supported_executor_methods(control_type: str = None):
        if control_type is None:
            return SUPPORTED_EXECUTOR_METHODS.copy()
        return SUPPORTED_EXECUTOR_METHODS.get(control_type, [])

    @staticmethod
    def get_supported_assertion_methods(control_type: str = None):
        if control_type is None:
            return SUPPORTED_ASSERTION_METHODS.copy()
        return SUPPORTED_ASSERTION_METHODS.get(control_type, [])
