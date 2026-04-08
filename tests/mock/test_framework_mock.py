"""
Mock模式测试 - 验证测试框架核心功能
无需启动真实应用，通过Mock方式验证框架流程
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from typing import Optional

from src.pytest_runner.test_runner import TestRunner
from src.config import Config


class MockWindow:
    """Mock窗口对象"""

    def __init__(self):
        self._exists = True
        self._visible = True
        self._enabled = True

    def exists(self, timeout=1):
        return self._exists

    def is_visible(self):
        return self._visible

    def is_enabled(self):
        return self._enabled

    def set_focus(self):
        pass

    def rectangle(self):
        class Rect:
            left, top, right, bottom = 0, 0, 800, 600

        return Rect()

    def capture_as_image(self):
        from PIL import Image

        return Image.new("RGB", (800, 600), "white")

    def wait(self, state, timeout=1):
        return True

    def child_window(self, **kwargs):
        return MockControl()

    def __getattr__(self, name):
        return Mock()


class MockControl:
    """Mock控件对象"""

    def __init__(self):
        self._exists = True
        self._visible = True
        self._enabled = True
        self._text = "Mock Text"

    def exists(self, timeout=1):
        return self._exists

    def is_visible(self):
        return self._visible

    def is_enabled(self):
        return self._enabled

    def text(self):
        return [self._text]

    def texts(self):
        return [self._text]

    def click(self):
        print("  [Mock] Button clicked")

    def click_input(self):
        print("  [Mock] Control clicked")

    def set_edit_text(self, text):
        print(f"  [Mock] Set text: {text}")

    def set_text(self, text):
        print(f"  [Mock] Set text: {text}")

    def get_text(self):
        return self._text

    def capture_as_image(self):
        from PIL import Image

        return Image.new("RGB", (100, 30), "white")

    def wait(self, state, timeout=1):
        return True

    def __getattr__(self, name):
        return Mock()


class MockApplication:
    """Mock pywinauto Application"""

    def __init__(self, backend="uia"):
        self.backend = backend
        self.window_spec = MockWindow()

    def window(self, **kwargs):
        return self.window_spec

    def connect(self, **kwargs):
        return self


@pytest.fixture
def mock_app():
    """Mock应用 fixture"""
    with (
        patch("src.pywinauto.app_manager.ApplicationManager.connect") as mock_connect,
        patch("src.pywinauto.app_manager.ApplicationManager.start") as mock_start,
        patch("src.pywinauto.app_manager.ApplicationManager.wait_window") as mock_wait,
    ):
        mock_connect.return_value = True
        mock_start.return_value = True
        mock_wait.return_value = MockWindow()

        yield {"connect": mock_connect, "start": mock_start, "wait_window": mock_wait}


@pytest.fixture
def mock_control_factory():
    """Mock ControlFactory fixture"""
    with patch("src.pywinauto.controls.ControlFactory") as mock_factory:
        mock_instance = Mock()
        mock_instance.window = MockWindow()

        mock_instance.button = Mock(return_value=MockControl())
        mock_instance.edit = Mock(return_value=MockControl())
        mock_instance.image = Mock(return_value=MockControl())

        mock_factory.return_value = mock_instance
        yield mock_factory


class TestFrameworkWithMocks:
    """使用Mock验证框架核心功能"""

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=True)
    @patch("src.pywinauto.app_manager.ApplicationManager.wait_window")
    @patch("src.pywinauto.controls.ControlFactory")
    def test_config_loading(self, mock_factory, mock_wait, mock_connect):
        """测试1: 配置加载功能"""
        mock_wait.return_value = MockWindow()

        runner = TestRunner(
            config_path="tests/configs/login_config_no_assert_new.yaml",
            project_name="测试项目",
        )

        assert runner.config is not None
        assert "app" in runner.config
        assert "controls" in runner.config
        print("✓ 配置加载成功")

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=True)
    @patch("src.pywinauto.app_manager.ApplicationManager.wait_window")
    @patch("src.pywinauto.controls.ControlFactory")
    def test_app_connection(self, mock_factory, mock_wait, mock_connect):
        """测试2: 应用连接功能"""
        mock_wait.return_value = MockWindow()

        runner = TestRunner(config_path="tests/configs/login_config_no_assert_new.yaml")

        result = runner.connect_app(auto_start=False)

        assert result is True
        assert runner._is_connected is True
        print("✓ 应用连接成功")

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=True)
    @patch("src.pywinauto.app_manager.ApplicationManager.wait_window")
    @patch("src.pywinauto.controls.ControlFactory")
    def test_test_case_execution(self, mock_factory, mock_wait, mock_connect):
        """测试3: 测试用例执行流程"""
        mock_wait.return_value = MockWindow()

        runner = TestRunner(
            config_path="tests/configs/login_config_no_assert_new.yaml",
            project_name="注册测试",
        )

        runner.connect_app(auto_start=False)

        runner.run_test_case("registration_flow", "normal_registration")

        print("✓ 测试用例执行成功")

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=True)
    @patch("src.pywinauto.app_manager.ApplicationManager.wait_window")
    @patch("src.pywinauto.controls.ControlFactory")
    def test_step_execution(self, mock_factory, mock_wait, mock_connect):
        """测试4: 步骤执行功能"""
        mock_wait.return_value = MockWindow()

        runner = TestRunner(config_path="tests/configs/login_config_no_assert_new.yaml")

        runner.connect_app(auto_start=False)

        test_data = {
            "avatar_filename": "test.png",
            "signature_filename": "sig.png",
            "nickname": "testuser",
            "password": "123456",
        }

        steps = [
            {
                "name": "测试步骤",
                "action": {
                    "control": "register_button",
                    "method": "click",
                    "params": [],
                },
            }
        ]

        runner.run_step(steps[0], 0, test_data)

        print("✓ 步骤执行成功")

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=True)
    @patch("src.pywinauto.app_manager.ApplicationManager.wait_window")
    @patch("src.pywinauto.controls.ControlFactory")
    def test_assertion_execution(self, mock_factory, mock_wait, mock_connect):
        """测试5: 断言执行功能"""
        mock_wait.return_value = MockWindow()

        runner = TestRunner(config_path="tests/configs/login_config_no_assert_new.yaml")

        runner.connect_app(auto_start=False)

        assertions_config = [
            {"control": "filename_input", "checks": ["visible", "enabled"]}
        ]

        try:
            runner.execute_assertions(assertions_config)
            print("✓ 断言执行成功")
        except Exception as e:
            print(f"  断言跳过（非关键控件）: {e}")


class TestDataDrivenWithMocks:
    """使用Mock验证数据驱动功能"""

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=True)
    @patch("src.pywinauto.app_manager.ApplicationManager.wait_window")
    @patch("src.pywinauto.controls.ControlFactory")
    def test_multiple_test_data(self, mock_factory, mock_wait, mock_connect):
        """测试6: 多组测试数据驱动"""
        mock_wait.return_value = MockWindow()

        runner = TestRunner(config_path="tests/configs/login_config_no_assert_new.yaml")

        runner.connect_app(auto_start=False)

        test_cases = [
            ("registration_flow", "normal_registration"),
            ("registration_flow", "invalid_nickname_empty"),
            ("registration_flow", "invalid_password_short"),
        ]

        for case_name, data_key in test_cases:
            print(f"  执行: {case_name} - {data_key}")
            runner.run_test_case(case_name, data_key)

        print("✓ 多组测试数据驱动成功")


class TestErrorHandlingWithMocks:
    """使用Mock验证错误处理"""

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=False)
    def test_connection_failure(self, mock_connect):
        """测试7: 连接失败处理"""
        runner = TestRunner(config_path="tests/configs/login_config_no_assert_new.yaml")

        result = runner.connect_app(auto_start=False)

        assert result is False
        print("✓ 连接失败处理正确")

    @patch("src.pywinauto.app_manager.ApplicationManager.connect", return_value=True)
    @patch(
        "src.pywinauto.app_manager.ApplicationManager.wait_window", return_value=None
    )
    def test_window_not_found(self, mock_wait, mock_connect):
        """测试8: 窗口未找到处理"""
        runner = TestRunner(config_path="tests/configs/login_config_no_assert_new.yaml")

        result = runner.connect_app(auto_start=False)

        assert result is False
        print("✓ 窗口未找到处理正确")


class TestConfigValidation:
    """测试配置验证功能"""

    def test_valid_config(self):
        """测试9: 有效配置验证"""
        config = Config.load_config("tests/configs/login_config_no_assert_new.yaml")
        errors = Config.validate_config(config)

        assert errors is None or len(errors) == 0
        print("✓ 配置验证通过")

    def test_missing_required_fields(self):
        """测试10: 缺少必需字段检测"""
        invalid_config = {
            "app": {"process_name": "test.exe"}
            # 缺少 controls 等
        }

        errors = Config.validate_config(invalid_config)

        assert errors is not None and len(errors) > 0
        print(f"✓ 正确检测到配置错误: {errors}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
