"""
异步测试示例
展示 pytest-asyncio 新版本特性
"""

import asyncio
from typing import Any, Dict, List

import pytest


# ==================== 基础异步测试 ====================
async def async_fetch_data(delay: float = 0.1) -> Dict[str, Any]:
    """模拟异步数据获取"""
    await asyncio.sleep(delay)
    return {"status": "success", "data": [1, 2, 3]}


@pytest.mark.asyncio
async def test_async_fetch_data():
    """传统方式：需要显式标记"""
    result = await async_fetch_data(0.05)
    assert result["status"] == "success"
    assert len(result["data"]) == 3


# ==================== asyncio_mode="auto" 新特性 ====================
# 在 pytest.ini 中配置 asyncio_mode = auto 后，无需显式标记
async def test_async_auto_mode():
    """
    pytest-asyncio 新版本支持 asyncio_mode="auto"
    配置后无需 @pytest.mark.asyncio 标记
    """
    result = await async_fetch_data(0.01)
    assert isinstance(result, dict)
    assert "data" in result


# ==================== 异步fixture ====================
@pytest.fixture
async def async_database_connection():
    """异步fixture - 模拟数据库连接"""
    print("建立异步数据库连接...")
    await asyncio.sleep(0.05)
    connection = {"connected": True, "pool_size": 10}

    yield connection

    # 清理
    print("关闭数据库连接...")
    connection["connected"] = False
    await asyncio.sleep(0.02)


@pytest.mark.asyncio
async def test_with_async_fixture(async_database_connection):
    """使用异步fixture的测试"""
    assert async_database_connection["connected"] is True
    assert async_database_connection["pool_size"] == 10

    # 模拟数据库操作
    await asyncio.sleep(0.03)
    assert True  # 操作成功


# ==================== 异步参数化测试 ====================
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "delay,expected_count",
    [
        (0.01, 3),
        (0.02, 3),
        (0.05, 3),
    ],
)
async def test_async_parametrized(delay, expected_count):
    """异步参数化测试"""
    result = await async_fetch_data(delay)
    assert len(result["data"]) == expected_count


# ==================== 并发异步测试 ====================
async def async_process_item(item: int) -> int:
    """模拟异步处理单个项目"""
    await asyncio.sleep(0.01)
    return item * 2


@pytest.mark.asyncio
async def test_concurrent_async_operations():
    """测试并发异步操作"""
    items = [1, 2, 3, 4, 5]

    # 并发处理所有项目
    tasks = [async_process_item(item) for item in items]
    results = await asyncio.gather(*tasks)

    assert results == [2, 4, 6, 8, 10]
    assert len(results) == len(items)


# ==================== 异步超时测试 ====================
@pytest.mark.asyncio
async def test_async_timeout():
    """异步操作超时测试"""
    with pytest.raises(asyncio.TimeoutError):
        # 设置超时为0.1秒
        await asyncio.wait_for(async_fetch_data(0.2), timeout=0.1)


# ==================== 异步mock测试 ====================
try:
    from unittest.mock import AsyncMock, patch

    @pytest.mark.asyncio
    async def test_async_mock():
        """异步mock测试"""
        mock_fetch = AsyncMock(return_value={"status": "mocked", "data": [99]})

        with patch(__name__ + ".async_fetch_data", mock_fetch):
            result = await async_fetch_data()

        assert result["status"] == "mocked"
        assert result["data"] == [99]
        mock_fetch.assert_awaited_once()

except ImportError:
    # Python < 3.8 兼容
    @pytest.mark.skip("AsyncMock requires Python 3.8+")
    @pytest.mark.asyncio
    async def test_async_mock():
        pass


# ==================== 异步事件循环fixture ====================
@pytest.fixture
def event_loop():
    """自定义事件循环fixture（高级用法）"""
    # 创建新的事件循环
    loop = asyncio.new_event_loop()
    yield loop
    # 清理
    loop.close()


@pytest.mark.asyncio
async def test_custom_event_loop(event_loop):
    """使用自定义事件循环"""
    # 当前测试使用提供的事件循环
    result = await async_fetch_data(0.01)
    assert result["status"] == "success"


# ==================== 异步类测试 ====================
class AsyncProcessor:
    """异步处理器类"""

    def __init__(self):
        self.processed_items = []

    async def process(self, item: int) -> int:
        """异步处理方法"""
        await asyncio.sleep(0.01)
        processed = item * 3
        self.processed_items.append(processed)
        return processed

    async def batch_process(self, items: List[int]) -> List[int]:
        """批量异步处理"""
        tasks = [self.process(item) for item in items]
        return await asyncio.gather(*tasks)


@pytest.mark.asyncio
class TestAsyncProcessor:
    """异步类测试"""

    @pytest.fixture
    async def processor(self):
        """异步类fixture"""
        return AsyncProcessor()

    async def test_single_process(self, processor):
        """测试单个异步处理"""
        result = await processor.process(5)
        assert result == 15
        assert 15 in processor.processed_items

    async def test_batch_process(self, processor):
        """测试批量异步处理"""
        items = [1, 2, 3, 4, 5]
        results = await processor.batch_process(items)

        assert results == [3, 6, 9, 12, 15]
        assert len(processor.processed_items) == len(items)


# ==================== 异步错误处理 ====================
class AsyncError(Exception):
    """自定义异步异常"""

    pass


async def async_operation_with_error(should_fail: bool) -> str:
    """可能失败的异步操作"""
    await asyncio.sleep(0.01)
    if should_fail:
        raise AsyncError("异步操作失败")
    return "成功"


@pytest.mark.asyncio
async def test_async_error_handling():
    """异步错误处理测试"""
    # 测试成功情况
    result = await async_operation_with_error(False)
    assert result == "成功"

    # 测试失败情况
    with pytest.raises(AsyncError) as exc_info:
        await async_operation_with_error(True)

    assert "异步操作失败" in str(exc_info.value)


# ==================== 配置说明 ====================
"""
要使 asyncio_mode="auto" 生效，需要在 pytest.ini 中添加：

[pytest]
asyncio_mode = auto

或者在 pyproject.toml 中添加：

[tool.pytest.ini_options]
asyncio_mode = "auto"

这样就不需要为每个异步测试添加 @pytest.mark.asyncio 标记。
"""

if __name__ == "__main__":
    # 运行异步测试
    pytest.main([__file__, "-v", "--tb=short", "--asyncio-mode=auto"])
