# Pytest New

基于 pytest 的自动化测试框架，集成 pywinauto 和 Allure 报告。

## 功能特性

- **Pytest 框架**: Python 测试框架
- **Pywinauto**: Windows UI 自动化测试
- **Allure 报告**: 美观的测试报告
- **YAML 配置**: 易于使用的测试用例配置

## 环境要求

- Python 3.10+
- Windows 操作系统

## 安装

```bash
pip install -r requirements.txt
```

## 运行测试

```powershell
# 运行所有测试
python -m pytest tests --alluredir=allure-results

# 或使用 PowerShell 脚本
.\run_test.ps1
```

## 生成 Allure 报告

```bash
allure generate allure-results -o allure-report
allure open allure-report
```

## 项目结构

```
pytest_new/
├── src/
│   ├── allure/           # Allure 辅助工具
│   ├── config/          # 配置解析
│   ├── pytest_runner/   # 测试运行器
│   └── pywinauto/       # UI 自动化
├── tests/
│   ├── configs/         # 测试配置 (YAML)
│   └── test_*.py       # 测试用例
├── requirements.txt    # Python 依赖
└── run_test.ps1        # 运行脚本
```

## 配置说明

测试用例定义在 `tests/configs/` 目录下的 YAML 文件中。

## YAML 配置模板

```yaml
# 自动化测试配置模板
# 版本: 1.0
# 框架: src目录下的控件和执行器

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

  edit_example:
    type: "edit"
    locator:
      title: "输入框标题"
      best_match: "Edit1"

# 测试数据
test_data:
  test_case_1:
    username: "test_user"
    password: "test_password"

# 测试用例
test_cases:
  test_case_1:
    description: "测试用例1描述"
    test_data: "test_case_1"

    # Allure报告配置
    epic: "模块名称"
    feature: "功能名称"
    story: "用户故事"
    severity: "normal"
    tags: ["标签1", "标签2"]
    suite: "测试套件"

    steps:
      - name: "step-001: 点击按钮"
        action:
          control: "button_example"
          method: "click"
          params: []
        assertions:
          - control: "button_example"
            checks: ["visible", "enabled"]
        timeout: "normal"

      - name: "step-002: 输入文本"
        action:
          control: "edit_example"
          method: "set_text"
          params: ["{{test_data.username}}"]
        assertions:
          - control: "edit_example"
            checks: ["visible", "enabled", "text_equal"]
        timeout: "normal"

# 等待时间配置
timeouts:
  short: 0.2
  normal: 0.5
  long: 1.0
```

### 控件类型 (controls)

| 类型 | 说明 |
|------|------|
| button | 按钮控件 |
| edit | 文本输入框 |
| image | 图片控件 |
| combobox | 下拉框 |
| listbox | 列表框 |
| tab | 标签页 |
| tree | 树形控件 |
| progressbar | 进度条 |
| slider | 滑块 |
| calendar | 日历 |
| statusbar | 状态栏 |
| menu | 菜单 |
| toolbar | 工具栏 |
| hyperlink | 超链接 |
| groupbox | 分组框 |
| scrollbar | 滚动条 |
| richedit | 富文本 |
| label | 标签 |
| dialog | 对话框 |

### Allure 报告配置

| 字段 | 说明 | 可选值 |
|------|------|--------|
| epic | 史诗 | - |
| feature | 功能 | - |
| story | 用户故事 | - |
| severity | 严重级别 | blocker, critical, normal, minor, trivial |
| tags | 自定义标签 | - |
| suite | 套件名称 | - |
| layer | 层级 | e2e, integration, unit |
