# 快速开始

## 环境要求

- Python 3.10+
- Windows 10+

## 安装依赖

```bash
pip install -r requirements.txt
```

或者使用 poetry：

```bash
poetry install
```

## 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
copy .env.example .env
```

## 运行测试

### 使用 Python

```bash
python -m pytest tests/
```

### 使用 CLI 工具

```bash
python scripts/cli.py -m login -mk smoke -e test
```

参数说明：
- `-m`: 指定测试模块（如 login）
- `-mk`: 指定 pytest 标签（如 smoke, regression）
- `-e`: 指定运行环境（dev/test/prod）
- `-c`: 指定测试用例名称
- `-n`: 并行进程数

### 使用脚本

```bash
run_test.bat -e test -m login
```

## 生成报告

```bash
allure generate allure-results -o allure-report
allure open allure-report
```

## 常用命令

```bash
# 运行指定标签的测试
pytest -m smoke

# 运行指定用例
pytest -k "test_login"

# 并行执行
pytest -n auto

# 生成覆盖率报告
pytest --cov=src tests/
```
