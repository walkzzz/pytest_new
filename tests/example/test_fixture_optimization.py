"""
Fixture 缓存优化示例
展示 pytest 7.x+ 新特性的用法
"""

import time
from typing import Any, Dict

import pytest


class HeavyResource:
    """模拟重量级资源（如数据库连接、大文件加载）"""

    def __init__(self):
        self.initialized = False
        self.data: Dict[str, Any] = {}

    def initialize(self) -> "HeavyResource":
        """模拟耗时初始化"""
        print("初始化重量级资源...")
        time.sleep(0.5)  # 模拟耗时操作
        self.data = {"loaded": True, "timestamp": time.time()}
        self.initialized = True
        return self

    def query(self, key: str) -> Any:
        """模拟查询操作"""
        if not self.initialized:
            self.initialize()
        return self.data.get(key)


# ==================== 传统方式（无缓存） ====================
@pytest.fixture(scope="session")
def heavy_resource_old():
    """传统session级fixture - 每次测试会话都重新初始化"""
    resource = HeavyResource()
    return resource.initialize()


# ==================== 新版本优化方式（带缓存） ====================
@pytest.fixture(scope="session")
def heavy_resource_cached():
    """
    优化版session级fixture - 支持懒加载缓存

    pytest 7.x+ 支持 cache=True 参数（实验性）
    实际使用中，session级fixture本身就有缓存效果
    这里展示如何手动实现智能缓存
    """
    _cached_resource = None

    def get_resource():
        nonlocal _cached_resource
        if _cached_resource is None:
            print("首次初始化重量级资源（缓存生效）")
            _cached_resource = HeavyResource().initialize()
        else:
            print("使用缓存的重量级资源")
        return _cached_resource

    return get_resource


# ==================== 参数化Fixture缓存示例 ====================
@pytest.fixture(scope="session", params=["config_v1", "config_v2", "config_v3"])
def app_config_cached(request):
    """
    参数化fixture的缓存优化
    每个参数值只初始化一次
    """
    config_type = request.param
    cache_key = f"app_config_{config_type}"

    # 简单的内存缓存（实际项目可用functools.lru_cache）
    if not hasattr(request.config, "_fixture_cache"):
        request.config._fixture_cache = {}

    if cache_key not in request.config._fixture_cache:
        print(f"初始化配置: {config_type}")
        time.sleep(0.1)  # 模拟耗时初始化
        if config_type == "config_v1":
            config = {"version": "1.0", "features": ["basic"]}
        elif config_type == "config_v2":
            config = {"version": "2.0", "features": ["basic", "advanced"]}
        else:
            config = {"version": "3.0", "features": ["basic", "advanced", "premium"]}

        request.config._fixture_cache[cache_key] = config
    else:
        print(f"使用缓存的配置: {config_type}")

    return request.config._fixture_cache[cache_key]


# ==================== 测试用例 ====================
def test_heavy_resource_old(heavy_resource_old):
    """测试传统fixture"""
    result = heavy_resource_old.query("timestamp")
    assert result is not None, f"重量级资源查询结果不应为None，实际得到: {result}"
    print(f"传统fixture查询结果: {result}")


def test_heavy_resource_cached(heavy_resource_cached):
    """测试缓存fixture"""
    resource = heavy_resource_cached()  # 调用函数获取资源
    result = resource.query("timestamp")
    assert result is not None, f"缓存资源查询结果不应为None，实际得到: {result}"
    print(f"缓存fixture查询结果: {result}")


def test_app_config_cached(app_config_cached):
    """测试参数化fixture缓存"""
    assert "version" in app_config_cached, f"配置中应包含'version'键，实际配置: {app_config_cached}"
    assert "features" in app_config_cached, f"配置中应包含'features'键，实际配置: {app_config_cached}"
    print(f"配置版本: {app_config_cached['version']}")


# ==================== 性能对比测试 ====================
@pytest.mark.benchmark
class TestFixturePerformance:
    """Fixture性能对比测试"""

    @pytest.fixture(autouse=True)
    def setup_timing(self):
        self.start_time = time.time()
        yield
        elapsed = time.time() - self.start_time
        print(f"测试执行时间: {elapsed:.3f}秒")

    def test_multiple_calls_cached(self, heavy_resource_cached):
        """多次调用缓存fixture"""
        for i in range(5):
            resource = heavy_resource_cached()
            assert (
                resource.query("loaded") is True
            ), f"第{i + 1}次调用缓存资源，loaded应为True，实际得到: {resource.query('loaded')}"

    def test_config_reuse(self, app_config_cached):
        """参数化fixture重用"""
        # 这里会展示缓存效果
        pass


# ==================== 高级缓存策略 ====================
try:
    from functools import lru_cache
except ImportError:
    # Python < 3.2 兼容
    lru_cache = None


if lru_cache:

    @lru_cache(maxsize=2)
    def load_config_file(config_path: str) -> Dict:
        """使用lru_cache缓存文件加载"""
        print(f"加载配置文件: {config_path}")
        time.sleep(0.2)  # 模拟文件读取
        return {"path": config_path, "content": "config_data"}

    @pytest.fixture
    def config_loader():
        """基于lru_cache的fixture"""
        return load_config_file

    def test_lru_cache_fixture(config_loader):
        """测试lru_cache优化的fixture"""
        config1 = config_loader("/path/to/config1.yaml")
        config2 = config_loader("/path/to/config2.yaml")
        config1_again = config_loader("/path/to/config1.yaml")  # 应该从缓存获取

        assert (
            config1 is config1_again
        ), f"LRU缓存应返回相同对象，但config1 ({id(config1)}) != config1_again ({id(config1_again)})"
        assert (
            config1 is not config2
        ), f"不同配置路径应返回不同对象，但config1 ({id(config1)}) == config2 ({id(config2)})"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
