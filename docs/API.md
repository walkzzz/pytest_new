# API 参考文档

本框架基于 pytest 和 pywinauto 构建，提供完整的 Windows UI 自动化测试能力。

## 核心模块架构

```
src/
├── core/                    # 核心基类
│   ├── base_test.py        # 测试基类
│   └── base_page.py        # 页面对象基类
├── config/                 # 配置管理
│   ├── settings.py         # 应用设置
│   ├── parser.py           # 配置解析器
│   └── yaml_loader.py      # YAML加载器
├── pywinauto/              # UI自动化扩展
│   ├── controls/           # 控件封装
│   ├── assertions/         # 断言扩展
│   ├── action_executors/   # 操作执行器
│   └── app_manager/        # 应用管理
├── pytest_runner/          # 测试运行器
├── utils/                  # 工具类
└── test_utils/             # 测试工具
```

## 核心模块详解

### 1. Core 模块 (`src/core/`)

#### `BaseTest` 类 (`base_test.py`)
所有测试用例的基类，集成 pytest fixture 和 UI 自动化能力。

```python
from src.core.base_test import BaseTest

class TestLogin(BaseTest):
    """登录功能测试"""
    
    def test_valid_login(self):
        """有效登录测试"""
        # 继承自 BaseTest 的方法和属性
        self.launch_app()  # 启动应用
        self.login_page.login("user", "pass")
        self.assert_home_page_loaded()
```

**主要方法**:
- `launch_app()`: 启动被测应用
- `close_app()`: 关闭应用
- `take_screenshot(name)`: 截图
- `log_message(message, level)`: 记录日志

#### `BasePage` 类 (`base_page.py`)
页面对象模式基类，封装 UI 控件操作。

```python
from src.core.base_page import BasePage
from src.pywinauto.controls import Button, TextBox

class LoginPage(BasePage):
    """登录页面"""
    
    def __init__(self, app):
        super().__init__(app)
        self.username = TextBox(self.app, locator={"title": "用户名"})
        self.password = TextBox(self.app, locator={"title": "密码"})
        self.login_btn = Button(self.app, locator={"title": "登录"})
    
    def login(self, username, password):
        """执行登录操作"""
        self.username.set_text(username)
        self.password.set_text(password)
        self.login_btn.click()
```

### 2. Config 模块 (`src/config/`)

#### `Settings` 类 (`settings.py`)
统一配置管理，支持环境变量和配置文件。

```python
from src.config.settings import Settings

# 获取配置实例
config = Settings()

# 访问配置
app_name = config.app.name
timeout = config.timeout.normal
log_level = config.logging.level

# 环境特定配置
if config.env == "production":
    base_url = config.production.base_url
else:
    base_url = config.development.base_url
```

**配置源优先级**:
1. 环境变量
2. `.env` 文件
3. `config/settings.yaml`
4. 默认值

#### `YamlLoader` 类 (`yaml_loader.py`)
YAML 配置文件加载器，支持热重载和嵌套配置。

```python
from src.config.yaml_loader import YamlLoader

loader = YamlLoader("tests/configs/login.yaml")
test_config = loader.load()

# 访问配置数据
steps = test_config["test_cases"]["login_flow"]["steps"]
data = test_config["test_data"]["valid_user"]
```

### 3. Pywinauto 扩展模块 (`src/pywinauto/`)

#### 控件库 (`src/pywinauto/controls/`)
封装 Windows 控件操作，提供统一接口。

```python
from src.pywinauto.controls import Button, TextBox, ComboBox, ListView

# 控件初始化
button = Button(app, locator={"title": "确定"})
textbox = TextBox(app, locator={"automation_id": "txtUsername"})
combobox = ComboBox(app, locator={"class_name": "ComboBox"})

# 控件操作
button.click()
textbox.set_text("test@example.com")
combobox.select("选项1")

# 控件状态检查
assert button.is_enabled()
assert textbox.is_visible()
assert combobox.has_item("选项1")
```

**支持的控件类型**:
- `Button`: 按钮
- `TextBox`: 文本框
- `ComboBox`: 下拉框
- `ListView`: 列表视图
- `CheckBox`: 复选框
- `RadioButton`: 单选按钮
- `Menu`: 菜单
- `TabControl`: 标签页

#### 断言库 (`src/pywinauto/assertions/`)
扩展的 UI 断言方法。

```python
from src.pywinauto.assertions import assert_visible, assert_enabled, assert_text_equals

# 基本断言
assert_visible(button, "按钮应可见")
assert_enabled(textbox, "文本框应可用")

# 文本断言
assert_text_equals(label, "预期文本", "标签文本应匹配")

# 复合断言
from src.pywinauto.assertions import AssertionBuilder

builder = AssertionBuilder(window)
builder.is_visible().has_text("欢迎").is_enabled().assert_all()
```

#### 操作执行器 (`src/pywinauto/action_executors/`)
标准化操作执行，支持重试和超时。

```python
from src.pywinauto.action_executors import ActionExecutor

executor = ActionExecutor(timeout=10, retry=3)

# 执行带重试的操作
result = executor.execute(
    action=lambda: button.click(),
    success_condition=lambda: success_indicator.is_visible(),
    error_message="点击按钮失败"
)
```

### 4. Pytest 集成模块 (`src/pytest_runner/`)

#### `TestRunner` 类 (`test_runner.py`)
测试运行器，支持自定义测试发现和执行。

```python
from src.pytest_runner.test_runner import TestRunner

runner = TestRunner(
    test_dir="tests",
    pattern="test_*.py",
    markers=["smoke", "regression"]
)

# 运行测试
results = runner.run(
    parallel=True,
    workers=4,
    report_dir="reports"
)

# 获取测试统计
print(f"通过: {results.passed}")
print(f"失败: {results.failed}")
print(f"跳过: {results.skipped}")
```

#### `BaseTestCase` 类 (`base_test_case.py`)
测试用例基类，集成常用 fixture 和工具。

```python
from src.pytest_runner.base_test_case import BaseTestCase

class LoginTestCase(BaseTestCase):
    """登录测试用例基类"""
    
    @pytest.fixture(scope="class")
    def test_user(self):
        """测试用户fixture"""
        return {"username": "test", "password": "pass123"}
    
    @pytest.mark.smoke
    def test_login_smoke(self, test_user):
        """冒烟测试"""
        result = self.login(test_user)
        assert result.success
```

### 5. Utils 工具模块 (`src/utils/`)

#### `Wait` 工具 (`wait.py`)
智能等待工具，支持多种等待条件。

```python
from src.utils.wait import Wait

wait = Wait(timeout=30, poll_interval=0.5)

# 等待条件成立
element = wait.until(
    condition=lambda: app.window(title="主窗口"),
    message="等待主窗口出现"
)

# 等待条件消失
wait.until_not(
    condition=lambda: loading_indicator.is_visible(),
    message="等待加载完成"
)
```

#### `Retry` 工具 (`retry.py`)
重试装饰器，处理临时性失败。

```python
from src.utils.retry import retry

@retry(max_attempts=3, delay=1, exceptions=(TimeoutError,))
def connect_to_service():
    """连接服务（自动重试）"""
    response = service.connect()
    if not response.ok:
        raise ConnectionError("连接失败")
    return response

# 使用重试
try:
    result = connect_to_service()
except Exception as e:
    print(f"重试后仍然失败: {e}")
```

#### `Config` 工具 (`config.py`)
配置辅助工具。

```python
from src.utils.config import load_config, save_config, merge_configs

# 加载配置
config = load_config("config.yaml")

# 合并配置
default_config = {"timeout": 30, "retry": 3}
user_config = {"timeout": 60}
merged = merge_configs(default_config, user_config)

# 保存配置
save_config(merged, "merged_config.yaml")
```

### 6. Test Utils 测试工具模块 (`src/test_utils/`)

#### Allure 集成 (`src/test_utils/allure/`)
Allure 报告增强工具。

```python
from src.test_utils.allure import attach_screenshot, attach_log, step

@step("用户登录操作")
def login_with_allure(username, password):
    """带Allure步骤的登录函数"""
    attach_log(f"开始登录，用户: {username}")
    
    try:
        result = login_page.login(username, password)
        attach_screenshot("登录成功截图")
        return result
    except Exception as e:
        attach_screenshot("登录失败截图")
        attach_log(f"登录失败: {str(e)}", level="error")
        raise
```

## Fixture 参考

框架预定义了大量 pytest fixture，可在 `conftest.py` 中找到。

### 应用级别 Fixture

```python
def test_with_app_fixtures(app, main_window, config):
    """使用应用fixture的测试"""
    # app: 启动的应用程序实例
    # main_window: 主窗口对象
    # config: 应用配置
    assert app.is_running()
    assert main_window.is_visible()
    assert config.app.name == "被测应用"
```

### 测试数据 Fixture

```python
def test_with_data_fixtures(test_data, user_factory, temp_dir):
    """使用数据fixture的测试"""
    # test_data: 从YAML加载的测试数据
    # user_factory: 用户数据工厂
    # temp_dir: 临时目录（自动清理）
    user = user_factory.create()
    assert user.is_valid()
    
    file_path = temp_dir / "test.txt"
    file_path.write_text("test")
    assert file_path.exists()
```

### UI 组件 Fixture

```python
def test_with_ui_fixtures(login_button, username_field, error_label):
    """使用UI组件fixture的测试"""
    # 这些fixture根据YAML配置自动创建
    username_field.set_text("testuser")
    login_button.click()
    
    if error_label.is_visible():
        error_text = error_label.get_text()
        pytest.fail(f"登录失败: {error_text}")
```

## 标记 (Markers) 参考

框架预定义的 pytest 标记：

| 标记 | 说明 | 示例 |
|------|------|------|
| `@pytest.mark.smoke` | 冒烟测试 | `@pytest.mark.smoke` |
| `@pytest.mark.regression` | 回归测试 | `@pytest.mark.regression` |
| `@pytest.mark.ui` | UI测试 | `@pytest.mark.ui` |
| `@pytest.mark.unit` | 单元测试 | `@pytest.mark.unit` |
| `@pytest.mark.integration` | 集成测试 | `@pytest.mark.integration` |
| `@pytest.mark.slow` | 慢速测试 | `@pytest.mark.slow` |
| `@pytest.mark.skip_ci` | 跳过CI | `@pytest.mark.skip_ci` |
| `@pytest.mark.benchmark` | 性能基准 | `@pytest.mark.benchmark` |
| `@pytest.mark.debug` | 调试专用 | `@pytest.mark.debug` |

## 命令行工具

### 脚本工具 (`scripts/cli.py`)

```bash
# 运行特定模块的测试
python scripts/cli.py -m login

# 运行带标记的测试
python scripts/cli.py -mk smoke

# 运行指定配置文件
python scripts/cli.py -c tests/configs/login.yaml

# 生成报告
python scripts/cli.py --report html,allure
```

### 运行脚本 (`run_test.ps1`, `run_test.bat`)

```powershell
# PowerShell
.\run_test.ps1 -Environment test -Module login

# Batch
run_test.bat -e test -m login
```

## 配置参考

### pytest.ini 配置

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = 
    -v
    --strict-markers
    --tb=short
    --alluredir=allure-results
    --clean-alluredir
    --html=reports/report.html
    --self-contained-html

markers =
    smoke: 冒烟测试（核心流程）
    regression: 回归测试
    # ... 更多标记
```

### YAML 配置结构

```yaml
app:
  process_name: "Application.exe"
  backend: "uia"
  main_window:
    title: "主窗口标题"
    state: "visible"

controls:
  button_ok:
    type: "button"
    locator:
      title: "确定"
      class_name: "Button"

test_data:
  valid_user:
    username: "testuser"
    password: "Test@123"

test_cases:
  login_success:
    description: "成功登录测试"
    steps:
      - name: "输入用户名"
        action:
          control: "username_field"
          method: "set_text"
          args: ["${test_data.valid_user.username}"]
```

## 扩展与自定义

### 自定义控件

```python
from src.pywinauto.controls.base_control import BaseControl

class CustomGridView(BaseControl):
    """自定义网格视图控件"""
    
    def get_row_count(self):
        """获取行数"""
        return self.element.item_count()
    
    def get_cell_value(self, row, column):
        """获取单元格值"""
        return self.element.get_item(row, column).text()
    
    def select_row(self, row):
        """选择行"""
        self.element.select(row)
```

### 自定义断言

```python
from src.pywinauto.assertions.base_assertion import BaseAssertion

class TableAssertion(BaseAssertion):
    """表格断言"""
    
    def has_row_count(self, expected_count):
        """验证行数"""
        actual = self.control.get_row_count()
        assert actual == expected_count, f"行数不符: {actual} != {expected_count}"
        return self
    
    def contains_text(self, text):
        """验证包含文本"""
        for row in range(self.control.get_row_count()):
            for col in range(self.control.get_column_count()):
                cell_value = self.control.get_cell_value(row, col)
                if text in cell_value:
                    return self
        pytest.fail(f"表格中未找到文本: {text}")
```

### 自定义 Fixture

```python
import pytest
from src.core.base_test import BaseTest

@pytest.fixture(scope="session")
def custom_database():
    """自定义数据库fixture"""
    db = DatabaseConnection()
    db.connect()
    
    yield db
    
    db.disconnect()

@pytest.fixture
def test_with_custom_fixture(custom_database):
    """使用自定义fixture的测试"""
    data = custom_database.query("SELECT * FROM users")
    assert len(data) > 0
```

## 故障排除

### 常见问题

1. **应用无法启动**
   - 检查 `process_name` 配置是否正确
   - 确认应用已安装且路径正确
   - 检查是否有权限问题

2. **控件找不到**
   - 使用 `Inspect.exe` 验证控件属性
   - 检查 `backend` 配置（"win32" 或 "uia"）
   - 尝试不同的定位策略

3. **测试不稳定**
   - 增加等待时间
   - 使用重试机制
   - 检查应用响应时间

4. **报告生成失败**
   - 确认 Allure 已安装
   - 检查输出目录权限
   - 查看 pytest 日志

### 调试技巧

```bash
# 启用详细日志
pytest -v --log-cli-level=DEBUG

# 显示本地变量
pytest --showlocals

# 进入调试模式
pytest --trace

# 仅运行失败用例
pytest --lf
```

## 版本兼容性

- **Python**: 3.10+
- **pytest**: 7.x, 8.x, 9.x
- **pywinauto**: 0.6.8+
- **Windows**: Windows 10/11

## 获取帮助

- 查看示例代码: `tests/example/`
- 阅读文档: `docs/`
- 报告问题: GitHub Issues

---

*最后更新: 2025年4月*  
*基于 pytest 9.0.2 和 pywinauto 0.6.8*