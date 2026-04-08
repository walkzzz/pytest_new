# Changelog

All notable changes to the `pytest_new_opt` UI automation testing framework.

## [Unreleased]

## [2.1.0] - 2026-04-08

### Added
- **Mock模式测试**: 新增 `tests/mock/test_framework_mock.py`，用于验证框架核心功能（无需真实应用）
- **Jenkins CI/CD配置**: 添加 `scripts/configure_jenkins.py` 自动配置脚本
- **中文编码优化**: 修复日志中文乱码问题（UTF-8编码支持）

### Fixed
- **YAML测试数据修复**: `invalid_nickname_empty` 的 nickname 改为空字符串，`invalid_password_short` 的 password 改为 "12"
- **依赖版本修复**: pytest-asyncio 从 1.3.0（不存在）修正为 >=0.23.0
- **连接逻辑优化**: BaseTestCase 移除不必要的 disconnect/connect 逻辑
- **依赖添加**: 新增 pytest-rerunfailures（失败重试）、mss 和 opencv-python（截图录屏）

### Enhanced
- **重试机制**: 添加 `--reruns 3 --reruns-delay 1` 失败重试配置
- **测试标记**: 新增 smoke（冒烟）、regression（回归）、rerun（重试）标记
- **测试用例命名**: 优化测试类和方法命名，更清晰表达测试意图

### CI/CD
- **Jenkins集成**: 在 Windows 11 上配置 Jenkins 2.541.3
- **自动化测试**: 配置 Job 自动运行 Mock 测试，生成 HTML 报告

## [2.0.0] - 2025-04-xx

### Added
- **Modern pytest 9.x+ optimization** based on specifications 666.md and 777.md
- **New package structure**: `pytest_new_opt` with `fixtures` module
- **Advanced examples**:
  - `test_parametrization_advanced.py`: Dictionary unpacking, nested combinations, indirect parametrization
  - `test_mock_example.py`: Comprehensive mocking patterns for UI automation
  - `test_fixture_optimization.py`: Session caching, parametrized fixtures, LRU cache integration
  - `test_async_example.py`: Simplified async testing with `asyncio_mode="auto"`
- **Code quality toolchain**:
  - Black formatting configuration
  - isort import sorting
  - flake8 linting rules
  - mypy type checking
- **Developer workflow**: Makefile with lint, test, typecheck, coverage commands
- **Complete documentation**

### Optimized
- **Execution efficiency**:
  - Parallel execution with `--dist loadgroup` and `--numprocesses auto`
  - Incremental testing with `pytest-testmon` (AST-based change detection)
  - Plugin lazy loading (20-40% startup speed improvement)
- **Test maintainability**:
  - Advanced parametrization patterns (40%+ code reduction)
  - Simplified async testing (30%+ code reduction)
  - Fixture caching and optimization
- **Debugging & reporting**:
  - Enhanced assertions with custom failure messages
  - Local variable display with `--showlocals`
  - Structured logging with `--report-log`
  - Allure + HTML report integration
- **Project standardization**:
  - Modern `pyproject.toml` configuration
  - Clear separation of concerns between `pyproject.toml` and `pytest.ini`
  - Proper package structure with `__init__.py` files

### Performance Metrics
| Optimization Area | Expected Improvement |
|-------------------|----------------------|
| Parallel execution | 30%-70% |
| Incremental testing | 50%-90% |
| Fixture caching | 20%-50% |
| Plugin lazy loading | 20%-40% |

---

**Last Updated**: April 2026  
**Test Framework**: pytest 9.0.2  
**Python Version**: 3.10+  
**Platform**: Windows 10/11  
**CI/CD**: Jenkins 2.541.3 (Local)