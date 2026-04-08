# 快速开始

## 环境要求

- Python 3.10+
- Windows 10/11
- Jenkins 2.541.3 (可选，用于 CI/CD)

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

### 1. Mock 测试（推荐先用）

无需真实应用，验证框架核心功能：

```bash
python -m pytest tests/mock/ -v
```

### 2. YAML 配置测试

使用 YAML 配置驱动 UI 测试：

```bash
python -m pytest tests/test_login_config_no_assert_new.py -v
```

### 3. 单元测试

```bash
python -m pytest tests/unit/ -v
```

### 4. 所有测试

```bash
python -m pytest tests/ --alluredir=allure-results
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `pytest tests/mock/` | 运行 Mock 测试 |
| `pytest -m smoke` | 运行冒烟测试 |
| `pytest -m regression` | 运行回归测试 |
| `pytest -k "test_login"` | 运行指定用例 |
| `pytest -n auto` | 并行执行 |
| `pytest --cov=src` | 生成覆盖率 |
| `pytest --reruns 3` | 失败重试 |
| `pytest --testmon` | 增量测试 |

## 生成报告

### HTML 报告（自动生成）

```bash
python -m pytest tests/mock/ -v --html=reports/report.html --self-contained-html
```

报告位置：`reports/report.html`

### Allure 报告

```bash
allure generate allure-results -o allure-report
allure open allure-report
```

## CI/CD - Jenkins 本地配置

### 1. 安装 Jenkins

```bash
choco install jenkins -y
```

### 2. 启动 Jenkins

```bash
net start Jenkins
```

访问：http://localhost:8080

### 3. 创建 Job

1. 点击 "New Item"
2. 输入名称：`pytest-pipeline`
3. 选择 "Freestyle project"
4. 配置构建步骤：

```batch
cd /d D:\TraeWorkspace\tryit\pytest_new_opt
python -m pip install -r requirements.txt
python -m pytest tests/mock/ -v --tb=short --html=reports/report.html --self-contained-html
```

5. 保存并点击 "Build Now"

### 4. 自动配置脚本

项目已提供自动配置脚本：

```bash
python scripts/configure_jenkins.py
```

## 测试类型说明

### Mock 测试

使用 Mock 模式验证框架功能，无需启动真实应用：

- 配置加载
- 应用连接
- 测试用例执行
- 步骤执行
- 断言执行
- 错误处理

### YAML 测试

使用 YAML 配置文件定义测试用例和数据：

```yaml
test_data:
  normal_registration:
    nickname: "test"
    password: "123456"

test_cases:
  registration_flow:
    steps:
      - name: "点击注册按钮"
        action:
          control: "register_button"
          method: "click"
```

### 单元测试

测试框架内部组件：

```bash
python -m pytest tests/unit/ -v
```

## 下一步

- 阅读 [项目架构](architecture.md) 了解整体设计
- 阅读 [使用指南](user-guide.md) 了解详细功能
- 阅读 [API 参考](api-reference.md) 了解接口文档