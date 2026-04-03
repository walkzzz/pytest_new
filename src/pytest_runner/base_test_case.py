import os
import pytest
import allure
from datetime import datetime
from src.pytest_runner.test_runner import TestRunner
from src.config.settings import Settings
from allure_commons.types import AttachmentType


class BaseTestCase:
    """测试基类 - 封装通用测试逻辑"""

    config_filename: str = None
    project_name: str = "自动化测试"
    build_name: str = None
    testplan_url: str = None
    runner: TestRunner = None
    config_path: str = None
    _app_started: bool = False

    @classmethod
    def _capture_screenshot(cls, name: str):
        """截取应用截图"""
        try:
            from PIL import ImageGrab
            import time

            os.makedirs(Settings.SCREENSHOT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(Settings.SCREENSHOT_DIR, filename)

            if (
                cls.runner
                and hasattr(cls.runner, "control_factory")
                and cls.runner.control_factory
            ):
                window = cls.runner.control_factory.window

                window.set_focus()
                time.sleep(0.3)

                rect = window.rectangle()
                bbox = (rect.left, rect.top, rect.right, rect.bottom)
                img = ImageGrab.grab(bbox=bbox)
                img.save(filepath)

                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        allure.attach(f.read(), name, AttachmentType.PNG)
                    try:
                        os.remove(filepath)
                    except:
                        pass
        except Exception as e:
            print(f"截图失败: {e}")

    @classmethod
    def setup_class(cls):
        """类级别setup - 启动应用并连接一次"""
        if cls.config_filename is None:
            raise ValueError("必须设置 config_filename 属性")

        tests_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        cls.config_path = os.path.join(tests_dir, "tests", cls.config_filename)
        cls.runner = TestRunner(
            config_path=cls.config_path,
            project_name=cls.project_name,
            build_name=cls.build_name,
            testplan_url=cls.testplan_url,
        )

        connected = cls.runner.connect_app(auto_start=True)

        with allure.step("启动应用"):
            cls._capture_screenshot("应用启动")

            if not connected:
                raise RuntimeError(
                    f"无法连接到应用: {cls.runner.app_config.get('process_name', 'unknown')}"
                )
        cls._app_started = True

    @classmethod
    def teardown_class(cls):
        """类级别teardown - 断开连接并关闭应用"""
        with allure.step("关闭应用"):
            if cls.runner and cls.runner._is_connected:
                cls._capture_screenshot("应用关闭")
                cls.runner.disconnect_app(close_app=True)

    def run_test_case(
        self, test_case_name: str, data_key: str = None, restart_app: bool = False
    ):
        """运行指定测试用例

        Args:
            test_case_name: 测试用例名称
            data_key: 测试数据 key
            restart_app: 是否在测试前重启应用（确保干净状态）
        """
        if restart_app:
            with allure.step("重启应用"):
                if self.runner._is_connected:
                    self.runner.disconnect_app(close_app=True)
                self.runner.connect_app(auto_start=True)
        else:
            if self.runner._is_connected:
                self.runner.disconnect_app(close_app=False)
            if not self.runner.connect_app(auto_start=False):
                self.runner.connect_app(auto_start=True)

        self.runner.run_test_case(test_case_name, data_key)

    def run_all_test_cases(self):
        """运行所有测试用例"""
        self.runner.run_all_test_cases()
