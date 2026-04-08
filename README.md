# Pytest New

基于 pytest 的自动化测试框架，集成 pywinauto 和 Allure 报告，支持 YAML 配置和数据驱动测试。

## 功能特性

- **Pytest 9.x+**: 最新版 pytest 测试框架
- **Pywinauto**: Windows UI 自动化测试
- **Allure 报告**: 美观的测试报告 + HTML 报告
- **YAML 配置**: 易于使用的测试用例配置
- **数据驱动**: 支持参数化和数据工厂模式
- **并行执行**: 支持 pytest-xdist 并行测试
- **Mock 测试**: 支持无应用验证框架功能
- **CI/CD**: 集成 Jenkins 本地自动化

## 环境要求

- Python 3.10+
- Windows 10/11
- Jenkins 2.541.3 (可选，用于 CI/CD)

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

# 运行 Mock 测试（无需真实应用）
python -m pytest tests/mock/ -v

# 运行冒烟测试
pytest -m smoke

# 并行执行
pytest -n auto --dist loadgroup

# 失败重试
pytest --reruns 3
```

### 3. 生成报告

```bash
# Allure 报告
allure generate allure-results -o allure-report
allure open allure-report

# HTML 报告（自动生成）
# 报告位于 reports/report.html
```

## 项目结构

```
pytest_new_opt/
├── src/
│   ├── core/              # 核心基类
│   ├── config/            # 配置管理
│   ├── utils/             # 工具类
│   ├── exceptions.py      # 自定义异常
│   ├── pytest_runner/     # 测试运行器
│   └── pywinauto/         # UI 自动化
├── tests/
│   ├── configs/           # 测试配置 (YAML)
│   ├── test_data/         # 测试数据 (JSON)
│   ├── mock/              # Mock 测试
│   ├── unit/              # 单元测试
│   └── example/           # 示例测试
├── scripts/               # 辅助脚本
│   └── configure_jenkins.py  # Jenkins 配置
├── docs/                  # 文档
├── .github/workflows/     # CI/CD 配置
├── pytest.ini             # pytest 配置
├── pyproject.toml         # 项目配置
└── requirements.txt       # 依赖
```

## 测试类型

### 1. Mock 测试（推荐先用）

无需真实应用，验证框架核心功能：

```bash
python -m pytest tests/mock/ -v
```

测试用例：
- `test_config_loading` - 配置加载
- `test_app_connection` - 应用连接
- `test_test_case_execution` - 测试用例执行
- `test_step_execution` - 步骤执行
- `test_assertion_execution` - 断言执行
- `test_multiple_test_data` - 多组测试数据
- `test_connection_failure` - 连接失败处理
- `test_window_not_found` - 窗口未找到处理

### 2. YAML 配置测试

使用 YAML 配置驱动 UI 测试：

```bash
python -m pytest tests/test_login_config_no_assert_new.py -v
```

### 3. 单元测试

```bash
python -m pytest tests/unit/ -v
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `pytest -m smoke` | 运行冒烟测试 |
| `pytest -m regression` | 运行回归测试 |
| `pytest -k "test_login"` | 运行指定用例 |
| `pytest -n auto` | 并行执行 |
| `pytest --cov=src` | 生成覆盖率 |
| `pytest --reruns 3` | 失败重试 |
| `pytest --testmon` | 增量测试 |

## 测试标记

| 标记 | 说明 |
|------|------|
| `@pytest.mark.smoke` | 冒烟测试（核心流程） |
| `@pytest.mark.regression` | 回归测试 |
| `@pytest.mark.slow` | 慢速测试 |
| `@pytest.mark.ui` | UI测试用例 |
| `@pytest.mark.unit` | 单元测试用例 |
| `@pytest.mark.rerun` | 失败重试测试 |
| `@pytest.mark.skip_ci` | 跳过CI执行 |

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

## CI/CD

### Jenkins 本地配置

1. 安装 Jenkins：`choco install jenkins -y`
2. 访问 http://localhost:8080
3. 创建 Job，配置构建步骤：
   ```batch
   cd /d D:\TraeWorkspace\tryit\pytest_new_opt
   python -m pip install -r requirements.txt
   python -m pytest tests/mock/ -v --tb=short --html=reports/report.html
   ```
4. 构建结果：SUCCESS

### GitHub Actions

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

## 文档

- [快速开始](docs/quick-start.md)
- [项目架构](docs/architecture.md)
- [使用指南](docs/user-guide.md)
- [API 参考](docs/api-reference.md)
- [并行测试优化](docs/parallel-testing-optimization.md)
- [断言与调试优化](docs/assertion-debugging-optimization.md)
- [更新日志](CHANGELOG.md)

## 优化功能

### 🚀 执行效率优化
- **智能并行执行**: 支持 `--dist loadgroup` 负载均衡
- **增量测试**: 集成 `pytest-testmon`
- **失败重试**: 集成 `pytest-rerunfailures`

### 📝 测试可维护性
- **Mock测试**: 无需真实应用验证框架
- **YAML配置**: 声明式测试用例
- **数据驱动**: 参数化测试

### 🔧 调试与报告增强
- **HTML报告**: 自动生成测试报告
- **Allure报告**: 丰富的测试报告
- **中文日志**: UTF-8 编码支持

### 📈 性能预期
| 优化项 | 预期性能提升 |
|--------|--------------|
| 并行执行 | 30%-70% |
| 增量测试 | 50%-90% |
| 失败重试 | 减少 flaky 测试 |

---

**版本**: 2.1.0  
**更新日期**: 2026-04-08  
**框架**: pytest 9.0.2  
**Python**: 3.10+  
**平台**: Windows 10/11  
**CI/CD**: Jenkins 2.541.3