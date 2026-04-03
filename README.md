# Pytest New

基于 pytest 的自动化测试框架，集成 pywinauto 和 Allure 报告。

## 功能特性

- **Pytest 框架**: Python 测试框架
- **Pywinauto**: Windows UI 自动化测试
- **Allure 报告**: 美观的测试报告
- **YAML 配置**: 易于使用的测试用例配置
- **数据驱动**: 支持参数化和数据工厂模式
- **并行执行**: 支持 pytest-xdist 并行测试

## 环境要求

- Python 3.10+
- Windows 操作系统

## 安装

```bash
pip install -r requirements.txt
```

或使用 poetry：

```bash
poetry install
```

## 快速开始

### 1. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
copy .env.example .env
```

### 2. 运行测试

```powershell
# 运行所有测试
python -m pytest tests --alluredir=allure-results

# 使用 CLI 工具
python scripts/cli.py -m login -mk smoke

# 使用 PowerShell 脚本
.\run_test.ps1

# 使用批处理脚本
run_test.bat -e test
```

### 3. 生成报告

```bash
# Allure 报告
allure generate allure-results -o allure-report
allure open allure-report

# HTML 报告 (自动生成)
# 报告位于 reports/report.html
```

## 运行命令

| 命令 | 说明 |
|------|------|
| `pytest -m smoke` | 运行冒烟测试 |
| `pytest -m regression` | 运行回归测试 |
| `pytest -k "test_login"` | 运行指定用例 |
| `pytest -n auto` | 并行执行 |
| `pytest --cov=src` | 生成覆盖率 |

## 项目结构

```
pytest_new/
├── src/
│   ├── core/              # 核心基类
│   ├── config/            # 配置管理
│   ├── utils/             # 工具类
│   ├── exceptions.py      # 自定义异常
│   ├── pytest_runner/     # 测试运行器
│   └── pywinauto/         # UI 自动化
├── tests/
│   ├── configs/           # 测试配置 (YAML)
│   ├── locators/          # 元素定位器
│   └── test_*.py          # 测试用例
├── fixtures/              # 可复用 fixture
├── data/                  # 测试数据
├── scripts/               # 辅助脚本
├── docs/                  # 文档
├── .github/workflows/     # CI/CD 配置
├── pytest.ini             # pytest 配置
├── pyproject.toml         # 项目配置
└── requirements.txt       # 依赖
```

## 配置说明

测试用例定义在 `tests/configs/` 目录下的 YAML 文件中。

## YAML 配置模板

```yaml
# 自动化测试配置模板

# 应用配置
app:
  process_name: "应用进程名.exe"
  backend: "uia"
  main_window:
    title: "主窗口标题"
    state: "visible"

# 控件配置
controls:
  button_example:
    type: "button"
    locator:
      title: "按钮文本"

# 测试数据
test_data:
  test_case_1:
    username: "test_user"
    password: "test_password"

# 测试用例
test_cases:
  test_case_1:
    description: "测试用例1描述"
    steps:
      - name: "step-001: 点击按钮"
        action:
          control: "button_example"
          method: "click"
        timeout: "normal"
```

## 常用标记

| 标记 | 说明 |
|------|------|
| `@pytest.mark.smoke` | 冒烟测试 |
| `@pytest.mark.regression` | 回归测试 |
| `@pytest.mark.slow` | 慢速测试 |

## CI/CD

项目已配置 GitHub Actions，每次 push 会自动运行测试。

## 核心规范

### 测试用例规范
- **命名规范**: `test_业务场景_条件_预期结果`（示例：`test_user_login_invalid_password_shows_error`）
- **结构规范**: 每个测试用例只测试一个业务场景，避免多重断言
- **断言原则**: 先状态码（如UI状态），后业务字段

### Fixture 作用域规范
- **session级**: 全局资源（如应用启动、数据库连接）
- **module级**: 模块共享资源（如用户配置）
- **function级**: 用例独立资源（如临时测试数据）

### 标记使用规范
- `@pytest.mark.smoke`: 冒烟测试（核心流程）
- `@pytest.mark.regression`: 回归测试
- `@pytest.mark.ui`: UI测试用例
- `@pytest.mark.unit`: 单元测试用例
- `@pytest.mark.skip_ci`: 跳过CI执行（用于本地调试）

## 最佳实践示例

参考 `tests/example/test_user_auth_best_practice.py` 了解完整的测试用例最佳实践。

## 文档

- [快速开始](docs/快速开始.md)
- [项目架构](docs/项目架构.md)
- [使用指南](docs/使用指南.md) - 详细使用说明
- [API 参考](docs/API.md) - 核心模块接口文档
- [并行测试优化](docs/并行测试优化.md)
- [断言与调试优化](docs/断言与调试优化.md)
- [优化实施总结](优化实施总结.md)

## 优化功能

基于 pytest 7.x/8.x+ 新特性的优化功能已全面集成：

### 🚀 执行效率优化
- **智能并行执行**: 支持 `--dist loadgroup` 负载均衡，CPU核心自适应
- **增量测试**: 集成 `pytest-testmon`，仅运行受代码变更影响的测试
- **Fixture缓存**: 会话级fixture缓存，减少重复初始化

### 📝 测试可维护性
- **高级参数化**: 字典解包、嵌套组合、间接参数化等高级模式
- **异步测试简化**: `asyncio_mode="auto"` 自动检测异步测试，无需手动标记
- **插件懒加载**: pytest 8.x+ 插件懒加载，启动速度提升20%-40%

### 🔧 调试与报告增强
- **智能断言**: 自定义断言失败信息，结构化数据断言优化
- **本地变量展示**: `--showlocals` 自动展示失败用例的变量值
- **精准调试**: `--trace` 精准断点，条件断点支持

### 🏗️ CI/CD 集成优化
- **快速失败策略**: `--exitfirst` 在CI中快速失败，节省资源
- **多版本矩阵**: 支持多Python版本测试矩阵
- **报告集成**: HTML报告 + Allure报告自动生成

### 📚 示例与文档
- **示例代码**: 查看 `tests/example/` 目录下的完整示例
- **详细文档**: 参考 `docs/` 目录下的优化指南
- **最佳实践**: 遵循 `tests/example/test_user_auth_best_practice.py` 中的模式

### 🚦 快速使用
```bash
# 并行执行优化
pytest -n auto --dist loadgroup

# 增量测试（仅运行受影响的用例）
pytest --testmon

# 异步测试（自动检测）
pytest tests/example/test_async_example.py

# 调试优化（显示本地变量）
pytest --showlocals --tb=short
```

### 📈 性能预期
| 优化项 | 预期性能提升 |
|--------|--------------|
| 并行执行 | 30%-70% |
| 增量测试 | 50%-90% |
| Fixture缓存 | 20%-50% |
| 插件懒加载 | 20%-40% |

查看 [优化实施总结](优化实施总结.md) 获取完整实施细节。
