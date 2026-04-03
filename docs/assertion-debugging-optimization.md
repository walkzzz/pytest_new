# 断言与调试优化指南

基于 pytest 7.x+/8.x+ 新特性的断言和调试优化。

## 断言体验优化

### 1. 自定义断言失败信息（pytest 7.0+）
```python
# 传统方式
def test_traditional():
    result = calculate_something()
    assert result == expected, f"计算结果错误: {result} != {expected}"

# 优化方式 - 更清晰的自定义信息
def test_optimized():
    result = calculate_something()
    assert result == expected, (
        f"计算结果验证失败\n"
        f"输入参数: {input_params}\n"
        f"预期结果: {expected}\n"
        f"实际结果: {result}\n"
        f"差异分析: {analyze_difference(result, expected)}"
    )
```

### 2. 断言重写钩子扩展
```python
# conftest.py
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_assertrepr_compare(config, op, left, right):
    """自定义断言比较的显示格式"""
    if isinstance(left, CustomObject) and isinstance(right, CustomObject) and op == "==":
        return [
            "CustomObject 比较失败:",
            f"  左值 ID: {left.id}",
            f"  右值 ID: {right.id}",
            f"  左值数据: {left.data[:50]}...",
            f"  右值数据: {right.data[:50]}...",
        ]
    
    if isinstance(left, dict) and isinstance(right, dict) and op == "==":
        # 比较两个字典，显示具体差异
        diff_keys = set(left.keys()) ^ set(right.keys())
        if diff_keys:
            return [
                "字典键不一致:",
                f"  左值独有键: {set(left.keys()) - set(right.keys())}",
                f"  右值独有键: {set(right.keys()) - set(left.keys())}",
            ]
```

### 3. 结构化数据断言优化
```python
import pytest

def test_json_response():
    """JSON响应断言优化"""
    response = {
        "status": "success",
        "data": {"user": {"id": 123, "name": "John"}},
        "meta": {"page": 1, "total": 100}
    }
    
    # 传统方式 - 多个assert
    assert response["status"] == "success"
    assert response["data"]["user"]["id"] == 123
    assert response["meta"]["page"] == 1
    
    # 优化方式 - 使用pytest-assume或单个assert
    with pytest.assume:
        assert response["status"] == "success"
        assert response["data"]["user"]["id"] == 123
        assert response["meta"]["page"] == 1
    
    # 或使用字典解构
    expected = {"status": "success", "data": {"user": {"id": 123}}}
    assert all(response[k] == v for k, v in expected.items() if k in response)
```

## 调试体验增强

### 1. 本地变量自动展示（--showlocals）
```bash
# 运行测试时自动显示失败用例的本地变量
pytest --showlocals

# 限制变量值显示长度（避免大对象刷屏）
pytest --showlocals --tb=short

# 在pytest.ini中配置
[pytest]
addopts = --showlocals --tb=short
```

### 2. 精准断点调试（--trace）
```bash
# 仅在指定用例触发pdb
pytest --trace test_specific_function

# 在特定标记的用例触发
pytest --trace -m integration

# 自定义调试器（如ipdb）
pytest --pdbcls=IPython.terminal.debugger:TerminalPdb --trace
```

### 3. 回溯信息优化
```bash
# 精简回溯，只显示核心失败链路
pytest --tb=short

# 仅显示失败行（最精简）
pytest --tb=line

# 显示完整回溯（传统方式）
pytest --tb=long

# 自动模式（智能选择）
pytest --tb=auto
```

## 高级调试配置

### 1. 自定义调试钩子
```python
# conftest.py
import pytest
import sys

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试报告钩子 - 增强调试信息"""
    outcome = yield
    report = outcome.get_result()
    
    if report.failed:
        # 收集额外调试信息
        debug_info = {
            "test_name": item.name,
            "location": f"{item.location[0]}:{item.location[1]}",
            "duration": call.duration,
            "locals": {}
        }
        
        # 只在需要时收集局部变量
        if hasattr(call, 'excinfo') and call.excinfo:
            tb = call.excinfo.traceback[-1]  # 获取失败点的栈帧
            if tb.frame:
                debug_info["locals"] = {
                    k: repr(v)[:100] for k, v in tb.frame.f_locals.items()
                }
        
        print(f"\n调试信息: {debug_info}")
```

### 2. 条件断点
```python
import pytest

def test_with_conditional_debug():
    """条件断点示例"""
    data = load_large_dataset()
    
    # 只在特定条件下进入调试
    if len(data) > 1000 and has_problem(data):
        pytest.set_trace()  # 条件断点
    
    process_data(data)
    assert validate_result(data)
```

### 3. 内存调试支持
```python
import pytest
import tracemalloc

@pytest.fixture(scope="function")
def memory_tracker():
    """内存使用跟踪fixture"""
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    
    yield
    
    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print("\n内存使用变化:")
    for stat in top_stats[:10]:  # 显示前10个
        print(f"{stat.count} blocks: {stat.size/1024:.1f} KiB")
        for line in stat.traceback.format()[:3]:
            print(f"  {line}")
    
    tracemalloc.stop()


def test_memory_usage(memory_tracker):
    """内存使用测试"""
    large_list = [i for i in range(100000)]
    processed = process_data(large_list)
    assert len(processed) == len(large_list)
```

## 配置优化

### pytest.ini 调试配置
```ini
[pytest]
# 回溯配置
tb = short

# 调试配置
showlocals = true
show_capture = no  # 不自动显示捕获的输出

# 超时配置（防止调试时超时）
timeout = 300
timeout_method = thread

# 标记配置
markers =
    debug: 调试专用测试（启用额外调试信息）
    no_debug: 跳过调试的测试
```

### 环境特定的调试配置
```bash
# 开发环境 - 启用完整调试
PYTEST_DEBUG=1 pytest --showlocals --tb=long -v

# CI环境 - 精简输出
PYTEST_CI=1 pytest --tb=short -q

# 生产调试 - 仅关键信息
PYTEST_PROD_DEBUG=1 pytest --tb=line --showlocals
```

## 实用调试命令

### 1. 快速重试失败用例
```bash
# 仅运行上次失败的用例
pytest --lf

# 运行上次失败和新加的用例
pytest --ff

# 收集失败用例但不运行
pytest --collect-only --lf
```

### 2. 交互式调试会话
```bash
# 进入pdb调试
pytest --pdb

# 使用ipdb（需要安装）
pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb

# 在特定失败时进入调试
pytest -x --pdb  # 第一次失败就进入调试
```

### 3. 性能调试
```bash
# 显示最慢的10个测试
pytest --durations=10

# 显示所有测试耗时
pytest --durations=0

# 性能分析（需要pytest-profiling）
pytest --profile --profile-svg
```

## 最佳实践

### 1. 分层断言策略
```python
def test_layered_assertions():
    """分层断言 - 从简单到复杂"""
    result = complex_operation()
    
    # 第一层：基本验证
    assert result is not None
    assert isinstance(result, dict)
    
    # 第二层：结构验证
    assert "status" in result
    assert "data" in result
    
    # 第三层：业务逻辑验证
    if result["status"] == "success":
        assert "user_id" in result["data"]
        assert result["data"]["user_id"] > 0
    else:
        assert "error" in result
        assert "message" in result["error"]
```

### 2. 调试信息收集
```python
import pytest
import logging

@pytest.fixture
def debug_logger():
    """调试日志收集器"""
    logger = logging.getLogger("test_debug")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def test_with_debug_logging(debug_logger):
    """带调试日志的测试"""
    debug_logger.debug("开始测试")
    
    try:
        result = risky_operation()
        debug_logger.debug(f"操作结果: {result}")
        assert validate_result(result)
    except Exception as e:
        debug_logger.error(f"测试失败: {e}", exc_info=True)
        raise
    
    debug_logger.debug("测试完成")
```

### 3. 智能失败处理
```python
import pytest

class TestSmartFailure:
    """智能失败处理示例"""
    
    @pytest.fixture(autouse=True)
    def failure_context(self, request):
        """测试失败上下文管理"""
        self.test_name = request.node.name
        self.start_time = time.time()
        
        yield
        
        if request.node.rep_call.failed:
            self._handle_failure(request.node.rep_call)
    
    def _handle_failure(self, report):
        """自定义失败处理"""
        duration = time.time() - self.start_time
        
        print(f"\n测试失败分析:")
        print(f"  测试名称: {self.test_name}")
        print(f"  执行时间: {duration:.2f}s")
        print(f"  失败类型: {report.excinfo.typename}")
        
        # 可以根据失败类型采取不同措施
        if "Timeout" in report.excinfo.typename:
            print("  建议: 增加超时时间或优化性能")
        elif "AssertionError" in report.excinfo.typename:
            print("  建议: 检查断言条件或测试数据")
        elif "ConnectionError" in report.excinfo.typename:
            print("  建议: 检查网络连接或服务状态")
```

## 工具集成

### 1. 与IDE集成
```yaml
# .vscode/launch.json (VS Code)
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["--tb=short", "--showlocals"],
      "console": "integratedTerminal"
    }
  ]
}
```

### 2. 与Docker集成
```dockerfile
# Docker调试配置
FROM python:3.10

# 安装调试工具
RUN pip install pytest pytest-remote pytest-timeout

# 设置调试环境变量
ENV PYTEST_DEBUG=1
ENV PYTHONPATH=/app

# 启动命令
CMD ["pytest", "--tb=short", "--showlocals", "-v"]
```

### 3. 与CI/CD集成
```yaml
# GitHub Actions调试配置
- name: 调试测试失败
  if: failure()
  run: |
    # 收集调试信息
    pytest --lf -v --tb=long --showlocals > debug.log
    
    # 上传调试日志
    echo "测试失败，查看debug.log获取详细信息"
    cat debug.log | tail -100
```