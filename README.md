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
