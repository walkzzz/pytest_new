"""
Custom pytest fixtures for UI automation testing.
"""

import functools
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator

import pytest

# 导入断言辅助工具
from .assertions import (
    assert_dict_contains,
    assert_dict_has,
    assert_eq,
    assert_equal,
    assert_list_eq,
    assert_list_equal,
    assert_with_context,
)

# ==================== 缓存装饰器 ====================


def cached_fixture(maxsize: int = 1):
    """
    缓存fixture结果的装饰器。

    适用于重量级资源初始化，确保在同一测试会话中只初始化一次。

    Args:
        maxsize: 缓存大小，默认为1（单例）

    Example:
        @cached_fixture()
        @pytest.fixture(scope="session")
        def heavy_resource():
            return HeavyResource()
    """

    def decorator(fixture_func):
        cache = {}

        @functools.wraps(fixture_func)
        def wrapper(*args, **kwargs):
            cache_key = (args, tuple(sorted(kwargs.items())))
            if cache_key not in cache:
                cache[cache_key] = fixture_func(*args, **kwargs)
            return cache[cache_key]

        return wrapper

    return decorator


# ==================== 通用夹具 ====================


@pytest.fixture(scope="session")
def temp_dir() -> Generator[str, None, None]:
    """全局临时目录（会话级）"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture(scope="function")
def env_vars() -> Generator[Dict[str, str], None, None]:
    """临时设置环境变量，用例结束后还原"""
    original_env = os.environ.copy()
    os.environ["TEST_MODE"] = "true"
    os.environ["PYTEST_UI_AUTOMATION"] = "true"

    yield dict(os.environ)

    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture(scope="session")
def project_root() -> Path:
    """项目根目录路径"""
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def test_data_dir(project_root: Path) -> Path:
    """测试数据目录路径，统一管理测试数据"""
    data_dir = project_root / "tests" / "test_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(scope="function")
def clean_logs_dir(project_root: Path) -> Generator[Path, None, None]:
    """清理日志目录"""
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    # 清理旧日志文件
    for log_file in logs_dir.glob("*.log"):
        try:
            log_file.unlink()
        except Exception:
            pass

    yield logs_dir


# ==================== UI自动化相关夹具 ====================


@pytest.fixture(scope="module")
def ui_app_config() -> Dict[str, Any]:
    """模块级UI应用配置，避免重复配置"""
    return {
        "process_name": "modulelogin.exe",
        "backend": "uia",
        "app_path": "D:\\Program Files\\CBIM\\modulelogin.exe",
        "start_timeout": 10,
    }


@pytest.fixture(scope="function")
def screenshot_context(project_root: Path, ui_app_config: Dict[str, Any]) -> Generator[Path, None, None]:
    """截图上下文管理器"""
    screenshot_dir = project_root / ui_app_config["screenshot_dir"]
    screenshot_dir.mkdir(exist_ok=True)

    yield screenshot_dir

    # 可选的清理逻辑
    # 保留截图供调试


# ==================== 测试数据夹具 ====================


@pytest.fixture(scope="function")
def temp_test_data(test_data_dir: Path) -> Generator[str, None, None]:
    """用例级临时测试数据（创建→用例执行→清理）"""
    import json
    import tempfile
    from datetime import datetime

    temp_file = tempfile.NamedTemporaryFile(suffix=".json", dir=test_data_dir, delete=False)
    temp_file.close()

    test_data = {
        "test_id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        "test_name": "ui_automation_test",
    }

    with open(temp_file.name, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    yield temp_file.name

    # 清理临时文件
    try:
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
    except Exception:
        pass


# ==================== 参数化夹具 ====================


@pytest.fixture(params=["uia", "win32"], ids=["UI自动化-uia", "UI自动化-win32"])
def backend_type(request):
    """参数化后端类型，测试不同后端兼容性"""
    return request.param


@pytest.fixture(params=[1, 3, 5], ids=["timeout_1s", "timeout_3s", "timeout_5s"])
def timeout_value(request):
    """参数化超时时间"""
    return request.param


# 导出断言辅助工具
__all__ = [
    # 原有夹具
    "temp_dir",
    "env_vars",
    "project_root",
    "test_data_dir",
    "clean_logs_dir",
    "ui_app_config",
    "screenshot_context",
    "temp_test_data",
    "backend_type",
    "timeout_value",
    "cached_fixture",
    # 断言辅助工具
    "assert_equal",
    "assert_eq",
    "assert_dict_contains",
    "assert_dict_has",
    "assert_list_equal",
    "assert_list_eq",
    "assert_with_context",
]
