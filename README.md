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
