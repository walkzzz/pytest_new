# 并行测试优化指南

基于 `pytest-xdist` 新版本（3.5.0+）的优化配置，提升测试执行效率。

## 核心优化策略

### 1. 智能负载均衡（--dist loadgroup）
替代简单的分片策略，按用例组进行负载均衡，避免"部分进程闲置、部分进程过载"。

```bash
# 按测试模块分组负载均衡
pytest -n auto --dist loadgroup

# 按测试类分组负载均衡  
pytest -n 4 --dist loadgroup --dist-group=class

# 自定义分组策略
pytest -n auto --dist loadscope --dist-scope=module
```

### 2. CPU核心自适应（--numprocesses auto）
自动检测系统CPU核心数，最大化资源利用率。

```bash
# 自动适配CPU核心（推荐）
pytest -n auto

# 指定进程数（如8核CPU）
pytest -n 8

# 留出部分核心给其他进程
pytest -n $(($(nproc) - 2))
```

### 3. 分组执行策略

| 策略 | 命令 | 适用场景 |
|------|------|----------|
| `loadgroup` | `--dist loadgroup` | 测试用例执行时间差异较大时 |
| `loadscope` | `--dist loadscope` | 同一模块/类的测试有共享状态时 |
| `loadfile` | `--dist loadfile` | 测试文件间完全独立时 |

## 配置示例

### pytest.ini 配置（可选）
```ini
[pytest]
# xdist 特定配置
xdist_group_scope = module
xdist_worker_timeout = 300
```

### 运行脚本示例
```bash
#!/bin/bash
# run_tests_parallel.sh

# 检测CPU核心数
CPU_CORES=$(python -c "import os; print(os.cpu_count())")
WORKERS=$((CPU_CORES > 4 ? CPU_CORES - 2 : CPU_CORES))

echo "使用 $WORKERS 个进程执行测试..."

# 运行测试（负载均衡模式）
pytest -n $WORKERS --dist loadgroup \
    --alluredir=allure-results \
    --html=reports/report.html \
    --self-contained-html
```

## 最佳实践

### 1. Fixture 作用域优化
- 会话级Fixture（`scope="session"`）自动在所有进程间共享
- 模块级Fixture（`scope="module"`）在同一个模块的测试间共享
- 避免在并行测试中使用函数级Fixture修改全局状态

### 2. 测试数据隔离
```python
import pytest
import tempfile
import os

@pytest.fixture(scope="function")
def temp_test_file():
    """每个测试函数独立的临时文件"""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        yield f.name
    # 测试后清理
    if os.path.exists(f.name):
        os.unlink(f.name)
```

### 3. 资源竞争处理
```python
import pytest
import threading

lock = threading.Lock()

@pytest.fixture(scope="function")
def shared_resource():
    """需要锁保护的共享资源"""
    with lock:
        # 初始化资源
        resource = initialize_resource()
        yield resource
        # 清理资源
        cleanup_resource(resource)
```

## 性能监控

### 查看执行统计
```bash
# 生成执行时间报告
pytest -n auto --durations=10

# 生成详细的xdist统计
pytest -n auto -v --tb=short | grep -E "(PASSED|FAILED|ERROR)"
```

### 资源使用监控
```bash
# Linux/Mac
top -p $(pgrep -f "pytest.*-n")

# 所有平台（使用psutil）
python -c "
import psutil
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
    if 'python' in proc.info['name'] and 'pytest' in ' '.join(proc.cmdline()):
        print(f\"PID: {proc.info['pid']}, CPU: {proc.info['cpu_percent']}%, Memory: {proc.info['memory_percent']}%\")
"
```

## 常见问题排查

### 1. 测试失败随机出现
- 检查测试是否依赖执行顺序（使用 `pytest-random-order` 插件验证）
- 确认共享资源是否有正确的锁保护
- 检查临时文件/目录是否唯一

### 2. 进程卡死或超时
```bash
# 增加超时时间
pytest -n auto --dist-timeout=300

# 设置worker超时
pytest -n auto --worker-timeout=60
```

### 3. 内存使用过高
- 减少并行进程数：`pytest -n 2`（替代 `auto`）
- 检查会话级Fixture是否缓存大对象
- 使用 `pytest-leaks` 插件检测内存泄漏

## CI/CD 集成

### GitHub Actions 配置
```yaml
- name: 并行运行测试
  run: |
    # 根据CI环境调整进程数
    if [ "$RUNNER_OS" == "Windows" ]; then
      WORKERS=2
    else
      WORKERS=4
    fi
    
    pytest -n $WORKERS --dist loadgroup \
      --cov=src --cov-report=xml \
      --junitxml=junit-report.xml
```

### 根据测试类型动态调整
```bash
#!/bin/bash
# 根据测试标记调整并行策略

if [[ "$TEST_TYPE" == "unit" ]]; then
    # 单元测试：高并发
    pytest -n auto --dist loadfile -m unit
elif [[ "$TEST_TYPE" == "integration" ]]; then
    # 集成测试：低并发（可能有外部依赖）
    pytest -n 2 --dist loadgroup -m integration
elif [[ "$TEST_TYPE" == "ui" ]]; then
    # UI测试：串行（避免UI冲突）
    pytest -m ui
fi
```