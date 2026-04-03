"""
Mock测试示例
展示如何在UI自动化测试中使用mock替换外部依赖
"""

import json
import os
import pathlib
import time
from unittest.mock import Mock, PropertyMock, call, patch

import pytest

# ==================== 基础Mock测试 ====================


def test_basic_mock():
    """基础Mock示例"""
    # 创建Mock对象
    mock_calculator = Mock()

    # 设置返回值
    mock_calculator.add.return_value = 5
    mock_calculator.multiply.return_value = 12

    # 调用Mock方法
    result_add = mock_calculator.add(2, 3)
    result_multiply = mock_calculator.multiply(3, 4)

    # 验证返回值
    assert result_add == 5
    assert result_multiply == 12

    # 验证方法调用
    mock_calculator.add.assert_called_once_with(2, 3)
    mock_calculator.multiply.assert_called_once_with(3, 4)


def test_mock_with_side_effect():
    """Mock side_effect用法"""
    mock_random = Mock()

    # side_effect可以是可迭代对象
    mock_random.randint.side_effect = [1, 2, 3, 4, 5]

    results = [mock_random.randint(1, 10) for _ in range(5)]
    assert results == [1, 2, 3, 4, 5]

    # side_effect也可以是函数
    def custom_side_effect(x, y):
        return x * y

    mock_random.multiply.side_effect = custom_side_effect
    assert mock_random.multiply(3, 4) == 12


def test_mock_exception():
    """Mock抛出异常"""
    mock_api = Mock()
    mock_api.request.side_effect = ConnectionError("网络连接失败")

    with pytest.raises(ConnectionError) as exc_info:
        mock_api.request("GET", "https://api.example.com")

    assert "网络连接失败" in str(exc_info.value)


# ==================== UI自动化Mock测试 ====================


class MockApplication:
    """模拟pywinauto Application对象"""

    def __init__(self):
        self.windows = {}
        self.process = None

    def start(self, process_path):
        """模拟启动应用"""
        self.process = Mock()
        self.process.pid = 12345
        return self

    def connect(self, **kwargs):
        """模拟连接应用"""
        self.process = Mock()
        self.process.pid = 67890
        return self

    def kill(self):
        """模拟杀死应用"""
        self.process = None

    def window(self, **kwargs):
        """模拟获取窗口"""
        window_mock = Mock()

        # 模拟窗口属性
        window_mock.exists.return_value = True
        window_mock.is_visible.return_value = True
        window_mock.is_enabled.return_value = True
        window_mock.texts.return_value = ["模拟窗口标题"]

        # 模拟控件查找
        def find_element(**locator):
            element_mock = Mock()
            element_mock.exists.return_value = True
            element_mock.is_visible.return_value = True
            element_mock.is_enabled.return_value = True
            element_mock.texts.return_value = [locator.get("title", "控件文本")]
            element_mock.click = Mock()
            element_mock.set_text = Mock()
            element_mock.get_text.return_value = "模拟文本"
            return element_mock

        window_mock.child_window = Mock(side_effect=find_element)

        return window_mock


def test_mock_pywinauto_application():
    """Mock pywinauto Application对象"""
    with patch("pywinauto.Application", autospec=True) as mock_app_class:
        # 创建模拟的Application实例
        mock_app_instance = MockApplication()
        mock_app_class.return_value = mock_app_instance

        # 模拟启动应用
        app = mock_app_class()
        started_app = app.start("C:\\Program Files\\App\\app.exe")

        assert started_app.process.pid == 12345

        # 模拟获取窗口
        window = started_app.window(title="主窗口")
        assert window.exists()
        assert window.is_visible()

        # 模拟查找控件
        button = window.child_window(title="登录按钮")
        button.click()

        # 验证点击被调用
        button.click.assert_called_once()


def test_mock_ui_control():
    """Mock UI控件操作"""
    # 模拟按钮控件
    mock_button = Mock()
    mock_button.exists.return_value = True
    mock_button.is_enabled.return_value = True
    mock_button.click = Mock()

    # 模拟文本框控件
    mock_textbox = Mock()
    mock_textbox.exists.return_value = True
    mock_textbox.is_enabled.return_value = True
    mock_textbox.set_text = Mock()
    mock_textbox.get_text.return_value = "输入的内容"

    # 测试按钮点击
    if mock_button.exists() and mock_button.is_enabled():
        mock_button.click()

    mock_button.click.assert_called_once()

    # 测试文本框输入
    mock_textbox.set_text("test@example.com")
    assert mock_textbox.get_text() == "输入的内容"
    mock_textbox.set_text.assert_called_once_with("test@example.com")


# ==================== 文件系统Mock测试 ====================


def test_mock_file_operations():
    """Mock文件操作"""
    with patch("builtins.open", create=True) as mock_open:
        # 模拟文件读取
        mock_file = Mock()
        mock_file.read.return_value = '{"user": "test", "status": "active"}'
        mock_open.return_value.__enter__.return_value = mock_file

        # 测试读取JSON文件
        with open("config.json", "r") as f:
            content = f.read()
            data = json.loads(content)

        assert data["user"] == "test"
        assert data["status"] == "active"

        # 验证文件打开
        mock_open.assert_called_once_with("config.json", "r")


def test_mock_os_path():
    """Mock os.path操作"""
    with patch("os.path.exists") as mock_exists:
        # 模拟文件存在
        mock_exists.return_value = True

        assert os.path.exists("/path/to/file.txt")
        mock_exists.assert_called_once_with("/path/to/file.txt")

    with patch("os.path.getsize") as mock_getsize:
        # 模拟文件大小
        mock_getsize.return_value = 1024

        size = os.path.getsize("/path/to/file.txt")
        assert size == 1024
        mock_getsize.assert_called_once_with("/path/to/file.txt")


def test_mock_pathlib():
    """Mock pathlib操作"""
    with patch("pathlib.Path") as MockPath:
        # 模拟Path对象
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.is_file.return_value = True
        mock_path.read_text.return_value = "文件内容"
        mock_path.write_text = Mock()

        MockPath.return_value = mock_path

        # 测试Path操作
        file_path = pathlib.Path("/test/file.txt")
        assert file_path.exists()
        assert file_path.is_file()
        assert file_path.read_text() == "文件内容"

        # 测试写入
        file_path.write_text("新内容")
        file_path.write_text.assert_called_once_with("新内容")  # type: ignore


# ==================== 网络请求Mock测试 ====================


def test_mock_requests():
    """Mock requests网络请求"""
    try:
        from unittest.mock import patch

        import requests

        with patch("requests.get") as mock_get:
            # 模拟成功响应
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": "test"}
            mock_response.text = '{"data": "test"}'
            mock_get.return_value = mock_response

            # 测试请求
            response = requests.get("https://api.example.com/data")
            assert response.status_code == 200
            assert response.json()["data"] == "test"

            mock_get.assert_called_once_with("https://api.example.com/data")

    except ImportError:
        pytest.skip("requests库未安装")


def test_mock_http_error():
    """Mock HTTP错误"""
    try:
        from unittest.mock import patch

        import requests

        with patch("requests.post") as mock_post:
            # 模拟错误响应
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
            mock_post.return_value = mock_response

            # 测试错误处理
            response = requests.post("https://api.example.com/create", json={})
            assert response.status_code == 404

            with pytest.raises(requests.HTTPError):
                response.raise_for_status()

    except ImportError:
        pytest.skip("requests库未安装")


# ==================== 数据库Mock测试 ====================


class MockDatabaseConnection:
    """模拟数据库连接"""

    def __init__(self):
        self.connected = False
        self.data = {}

    def connect(self):
        self.connected = True
        return self

    def disconnect(self):
        self.connected = False

    def query(self, sql, params=None):
        """模拟查询"""
        if not self.connected:
            raise ConnectionError("数据库未连接")

        # 模拟查询结果
        if "SELECT" in sql.upper():
            return [{"id": 1, "name": "测试用户"}]
        elif "INSERT" in sql.upper():
            return 1  # 影响的行数
        else:
            return 0

    def execute(self, sql, params=None):
        """模拟执行"""
        if not self.connected:
            raise ConnectionError("数据库未连接")
        return 1


def test_mock_database():
    """Mock数据库操作"""
    mock_db = MockDatabaseConnection()

    # 测试连接
    mock_db.connect()
    assert mock_db.connected

    # 测试查询
    users = mock_db.query("SELECT * FROM users")
    assert len(users) == 1  # type: ignore
    assert users[0]["name"] == "测试用户"  # type: ignore

    # 测试插入
    affected_rows = mock_db.execute("INSERT INTO users (name) VALUES (?)", ["新用户"])
    assert affected_rows == 1

    # 测试断开连接
    mock_db.disconnect()
    assert not mock_db.connected

    # 测试未连接时的错误
    with pytest.raises(ConnectionError):
        mock_db.query("SELECT * FROM users")


# ==================== 配置Mock测试 ====================


def test_mock_configuration():
    """Mock配置管理"""
    with patch("src.config.settings.Settings") as MockSettings:
        # 模拟配置对象
        mock_settings = Mock()
        mock_settings.app.name = "测试应用"
        mock_settings.app.path = "C:\\Test\\app.exe"
        mock_settings.timeout.normal = 30
        mock_settings.timeout.long = 60
        mock_settings.logging.level = "INFO"

        MockSettings.return_value = mock_settings

        # 测试配置访问
        config = MockSettings()
        assert config.app.name == "测试应用"
        assert config.app.path == "C:\\Test\\app.exe"
        assert config.timeout.normal == 30
        assert config.logging.level == "INFO"


# ==================== 时间相关Mock测试 ====================


def test_mock_time():
    """Mock时间相关操作"""
    with patch("time.time") as mock_time:
        # 模拟固定时间
        mock_time.return_value = 1609459200.0  # 2021-01-01 00:00:00

        current_time = time.time()
        assert current_time == 1609459200.0

        # 模拟时间流逝
        mock_time.side_effect = [1000.0, 1010.0, 1020.0]

        start = time.time()
        middle = time.time()
        end = time.time()

        assert start == 1000.0
        assert middle == 1010.0
        assert end == 1020.0


def test_mock_sleep():
    """Mock sleep操作"""
    with patch("time.sleep") as mock_sleep:
        # 模拟sleep，实际不等待
        mock_sleep.return_value = None

        _start = time.time()  # noqa: F841
        time.sleep(5)  # 应该立即返回
        _end = time.time()  # noqa: F841

        # 验证sleep被调用
        mock_sleep.assert_called_once_with(5)

        # 注意：由于sleep被mock，实际耗时接近0
        # 实际测试中可以根据需要断言耗时


# ==================== 异步Mock测试 ====================


@pytest.mark.asyncio
async def test_mock_async_function():
    """Mock异步函数"""

    async def mock_async_func():
        return "模拟结果"

    # 创建异步mock
    mock_async = Mock()
    mock_async.return_value = mock_async_func()

    # 或者使用AsyncMock（Python 3.8+）
    try:
        from unittest.mock import AsyncMock

        async_mock = AsyncMock()
        async_mock.return_value = {"status": "success"}

        result = await async_mock()
        assert result["status"] == "success"

    except ImportError:
        # Python < 3.8 回退方案
        pytest.skip("AsyncMock需要Python 3.8+")


# ==================== Fixture中的Mock ====================


@pytest.fixture
def mock_app_fixture():
    """提供Mock应用的fixture"""
    with patch("pywinauto.Application") as mock_app_class:
        mock_app = Mock()
        mock_app.start.return_value = mock_app
        mock_app.window.return_value.exists.return_value = True
        mock_app_class.return_value = mock_app

        yield mock_app


def test_with_mock_fixture(mock_app_fixture):
    """使用Mock fixture的测试"""
    # 直接使用fixture提供的mock对象
    app = mock_app_fixture
    app.start("app.exe")

    window = app.window(title="主窗口")
    assert window.exists()

    app.start.assert_called_once_with("app.exe")
    app.window.assert_called_once_with(title="主窗口")


# ==================== patch装饰器用法 ====================


@patch("os.getcwd")
def test_patch_decorator(mock_getcwd):
    """使用patch装饰器"""
    mock_getcwd.return_value = "/mock/directory"

    current_dir = os.getcwd()
    assert current_dir == "/mock/directory"
    mock_getcwd.assert_called_once()


@patch("os.listdir")
@patch("os.path.isdir")
def test_multiple_patch_decorators(mock_isdir, mock_listdir):
    """多个patch装饰器"""
    mock_isdir.return_value = True
    mock_listdir.return_value = ["file1.txt", "file2.txt"]

    if os.path.isdir("/mock"):
        files = os.listdir("/mock")
        assert files == ["file1.txt", "file2.txt"]

    mock_isdir.assert_called_once_with("/mock")
    mock_listdir.assert_called_once_with("/mock")


# ==================== 上下文管理器中的Mock ====================


def test_patch_context_manager():
    """在上下文管理器中使用patch"""
    original_value = os.getenv("TEST_VAR")

    with patch.dict("os.environ", {"TEST_VAR": "mock_value"}):
        # 在上下文内，环境变量被mock
        assert os.getenv("TEST_VAR") == "mock_value"

    # 在上下文外，环境变量恢复
    assert os.getenv("TEST_VAR") == original_value


# ==================== Mock属性访问 ====================


def test_mock_property():
    """Mock属性访问"""

    class User:
        @property
        def name(self):
            return "真实姓名"

    with patch.object(User, "name", new_callable=PropertyMock) as mock_name:
        mock_name.return_value = "Mock姓名"
        user = User()
        assert user.name == "Mock姓名"
        mock_name.assert_called_once()


# ==================== 验证Mock调用 ====================


def test_mock_assertions():
    """Mock断言验证"""
    mock_service = Mock()

    # 多次调用
    mock_service.process("item1")
    mock_service.process("item2")
    mock_service.process("item3")

    # 验证调用次数
    assert mock_service.process.call_count == 3

    # 验证至少调用一次
    mock_service.process.assert_called()

    # 验证最近一次调用
    mock_service.process.assert_called_with("item3")

    # 验证特定调用
    mock_service.process.assert_any_call("item1")

    # 验证调用参数
    calls = [call("item1"), call("item2"), call("item3")]
    mock_service.process.assert_has_calls(calls, any_order=False)


# ==================== 集成Mock示例 ====================


class TestLoginWithMocks:
    """使用Mock的登录测试示例"""

    def test_login_success_with_mocks(self):
        """Mock成功登录场景"""
        # Mock所有外部依赖
        with (
            patch("pywinauto.Application") as mock_app_class,
            patch("src.config.settings.Settings") as mock_settings_class,
            patch("time.sleep") as mock_sleep,
        ):
            # 设置mock返回值
            mock_app = Mock()
            mock_app.start.return_value = mock_app

            # 创建独立的mock控件
            mock_username = Mock()
            mock_username.exists.return_value = True
            mock_password = Mock()
            mock_password.exists.return_value = True
            mock_login = Mock()
            mock_login.exists.return_value = True

            # 设置child_window side_effect根据title返回不同的mock
            def child_window_side_effect(**kwargs):
                title = kwargs.get("title", "")
                if title == "用户名":
                    return mock_username
                elif title == "密码":
                    return mock_password
                elif title == "登录":
                    return mock_login
                else:
                    return Mock()

            window_mock = Mock()
            window_mock.child_window.side_effect = child_window_side_effect
            mock_app.window.return_value = window_mock

            mock_app_class.return_value = mock_app

            mock_settings = Mock()
            mock_settings.app.name = "测试应用"
            mock_settings_class.return_value = mock_settings

            # 模拟登录流程
            app = mock_app_class()
            app.start("app.exe")

            window = app.window(title="登录窗口")
            username_field = window.child_window(title="用户名")
            password_field = window.child_window(title="密码")
            login_button = window.child_window(title="登录")

            username_field.set_text("testuser")
            password_field.set_text("password123")
            login_button.click()

            # 验证交互
            username_field.set_text.assert_called_once_with("testuser")
            password_field.set_text.assert_called_once_with("password123")
            login_button.click.assert_called_once()

            # 验证没有调用sleep（如果业务逻辑中有）
            mock_sleep.assert_not_called()

    def test_login_failure_with_mocks(self):
        """Mock登录失败场景"""
        with patch("pywinauto.Application") as mock_app_class:
            mock_app = Mock()
            mock_app.start.return_value = mock_app

            # 模拟窗口存在但登录失败
            window_mock = Mock()
            window_mock.exists.return_value = True

            # 模拟错误消息控件
            error_label = Mock()
            error_label.exists.return_value = True
            error_label.get_text.return_value = "用户名或密码错误"

            window_mock.child_window.side_effect = lambda **kwargs: (
                error_label if kwargs.get("title") == "错误消息" else Mock()
            )

            mock_app.window.return_value = window_mock
            mock_app_class.return_value = mock_app

            # 测试登录失败处理
            app = mock_app_class()
            app.start("app.exe")

            window = app.window(title="登录窗口")
            error_element = window.child_window(title="错误消息")

            assert error_element.exists()
            assert error_element.get_text() == "用户名或密码错误"


# ==================== Mock最佳实践 ====================


def test_mock_best_practices():
    """Mock最佳实践示例"""

    # 1. 使用spec或autospec确保Mock对象接口正确
    from collections import OrderedDict

    with patch("collections.OrderedDict", autospec=True) as mock_dict_class:
        mock_dict = Mock(spec=OrderedDict)
        mock_dict.update.return_value = None
        mock_dict_class.return_value = mock_dict

        # 现在mock_dict具有OrderedDict的接口
        # 调用不存在的方法会抛出AttributeError

    # 2. 使用side_effect模拟复杂行为
    mock_complex = Mock()

    def complex_side_effect(arg):
        if arg == "success":
            return {"status": "success", "data": "result"}
        elif arg == "error":
            raise ValueError("Invalid argument")
        else:
            return {"status": "unknown"}

    mock_complex.process.side_effect = complex_side_effect

    # 3. 清理Mock状态（在测试之间）
    mock_complex.reset_mock()
    assert mock_complex.process.call_count == 0

    # 4. 验证Mock使用情况（避免过度Mock）
    # 只Mock真正的外部依赖，不要Mock被测代码的内部实现


if __name__ == "__main__":
    # 运行Mock测试
    pytest.main([__file__, "-v", "--tb=short"])

# ==================== Mock工具函数 ====================


def create_mock_window(**kwargs):
    """创建模拟窗口的辅助函数"""
    window_mock = Mock()
    window_mock.exists.return_value = kwargs.get("exists", True)
    window_mock.is_visible.return_value = kwargs.get("is_visible", True)
    window_mock.is_enabled.return_value = kwargs.get("is_enabled", True)
    window_mock.texts.return_value = kwargs.get("texts", ["窗口标题"])
    return window_mock


def create_mock_control(control_type="button", **kwargs):
    """创建模拟控件的辅助函数"""
    control_mock = Mock()

    # 通用属性
    control_mock.exists.return_value = kwargs.get("exists", True)
    control_mock.is_visible.return_value = kwargs.get("is_visible", True)
    control_mock.is_enabled.return_value = kwargs.get("is_enabled", True)
    control_mock.get_text.return_value = kwargs.get("text", "控件文本")

    # 类型特定方法
    if control_type == "button":
        control_mock.click = Mock()
    elif control_type == "textbox":
        control_mock.set_text = Mock()
        control_mock.get_text = Mock(return_value=kwargs.get("text", ""))
    elif control_type == "combobox":
        control_mock.select = Mock()
        control_mock.get_selected.return_value = kwargs.get("selected", "选项1")

    return control_mock
