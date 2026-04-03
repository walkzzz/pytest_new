针对 `walkzzz/pytest_new` 仓库（聚焦 pytest 测试工程化落地），以下是**更落地、可直接复用**的优化方案，覆盖「配置标准化、Fixture 最佳实践、用例质量、自动化提效、协作规范」五大核心，附完整代码示例和检查清单：

### 一、基础配置：标准化 + 避坑（可直接复制）
#### 1. 核心配置文件重构（替代零散配置）
删除冗余的 `setup.cfg`，统一用 `pyproject.toml`（PEP 621 标准）+ `pytest.ini` 分工：
- `pyproject.toml`（项目元信息 + 依赖 + 覆盖率）：
  ```toml
  [project]
  name = "pytest_new"
  version = "0.1.0"
  python = ">=3.8"
  dependencies = [
    "pytest==7.4.3",
    "pytest-cov==4.1.0",
    "pytest-xdist==3.5.0",
    "pytest-html==3.2.0",
    "allure-pytest==2.13.2"  # 可选，Allure报告
  ]

  [tool.pytest.ini_options]
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  python_classes = ["Test*"]
  python_functions = ["test_*"]
  addopts = """
    -v
    --tb=short  # 精简回溯信息
    --strict-markers  # 强制校验自定义标记
    --strict-config  # 强制校验配置
  """
  markers = [
    "smoke: 冒烟测试（核心流程）",
    "unit: 单元测试",
    "integration: 集成测试",
    "skip_ci: 跳过CI执行"
  ]

  [tool.coverage.run]
  source = ["src"]  # 仅统计业务代码（若有src目录）
  omit = [
    "src/*/__init__.py",
    "src/*/config.py",
    "tests/*"  # 排除测试代码
  ]

  [tool.coverage.report]
  show_missing = true  # 显示未覆盖代码行
  fail_under = 80      # 覆盖率低于80%则失败
  format = ["html", "xml"]  # 输出多格式报告
  ```
- `pytest.ini`（仅存 pytest 专属配置，兜底）：
  ```ini
  [pytest]
  # 若pyproject.toml配置不生效，用此兜底（优先级更低）
  cache_dir = .pytest_cache
  log_cli = true  # 运行时打印日志
  log_cli_level = INFO
  ```

#### 2. `.gitignore` 精准化（补充pytest专属）
```gitignore
# pytest 核心
.pytest_cache/
.coverage
coverage.xml
htmlcov/
pytest-report.html
allure-results/
allure-report/

# Python 通用
__pycache__/
*.py[cod]
*.pyd
*.pyo
.env/
venv/
.venv/
dist/
build/

# 测试临时文件
tests/test_data/*.tmp
tests/test_data/*.log
tests/test_data/*.json.bak
```

### 二、Fixture 设计：复用 + 分层（核心优化）
`conftest.py` 是 pytest 核心，避免Fixture冗余/作用域误用，以下是标准化设计：
```python
# tests/conftest.py
import pytest
import requests
from typing import Dict
import os

# -------------------------- 会话级Fixture（全局复用，仅初始化1次） --------------------------
@pytest.fixture(scope="session")
def api_session():
    """全局接口会话，复用连接池，减少耗时"""
    session = requests.Session()
    # 全局请求头
    session.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "pytest_new_test/0.1.0"
    })
    yield session
    # 会话结束后清理
    session.close()

@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录路径，统一管理测试数据"""
    dir_path = os.path.join(os.path.dirname(__file__), "test_data")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

# -------------------------- 模块级Fixture（每个.py文件复用） --------------------------
@pytest.fixture(scope="module")
def user_base_info() -> Dict:
    """模块级用户基础信息，避免重复造数据"""
    return {
        "username": "test_pytest_new",
        "email": "test@example.com"
    }

# -------------------------- 用例级Fixture（每个用例独立） --------------------------
@pytest.fixture(scope="function")
def temp_user(api_session, user_base_info):
    """用例级临时用户（创建→用例执行→删除）"""
    # 前置：创建用户
    create_resp = api_session.post("/api/users", json=user_base_info)
    user_id = create_resp.json()["id"]
    yield {"id": user_id, **user_base_info}
    # 后置：删除用户（清理脏数据）
    api_session.delete(f"/api/users/{user_id}")

# -------------------------- 参数化Fixture（动态传参） --------------------------
@pytest.fixture(params=["chrome", "firefox", "edge"], ids=["浏览器-Chrome", "浏览器-Firefox", "浏览器-Edge"])
def browser_type(request):
    """参数化浏览器类型，一键跑多浏览器用例"""
    return request.param
```

**Fixture 优化检查清单**：
- ✅ 所有Fixture归集到 `conftest.py`，禁止用例文件内定义通用Fixture；
- ✅ 严格区分作用域：session > module > function（避免session级Fixture修改导致用例污染）；
- ✅ 每个Fixture只做一件事（如`api_session`仅管理会话，`temp_user`仅管理用户生命周期）；
- ✅ 后置操作必须写（如关闭连接、删除测试数据），避免脏数据。

### 三、测试用例：解耦 + 精准 + 易读
#### 1. 用例命名&结构规范（示例）
拒绝模糊命名，采用「`test_业务场景_条件_预期结果`」：
```python
# tests/unit/test_user.py
import pytest

# 标记+参数化组合，覆盖多场景
@pytest.mark.unit
@pytest.mark.parametrize("password, expected_code", [
    ("123456", 200),          # 合法密码
    ("123", 400),             # 密码过短
    ("", 400),                # 空密码
    ("12345678901234567890", 400)  # 密码过长
], ids=["合法密码", "密码过短", "空密码", "密码过长"])
def test_user_register_password_check(api_session, password, expected_code):
    """测试用户注册-密码合法性校验"""
    # 步骤1：构造请求数据（仅必要数据，复用Fixture）
    req_data = {
        "username": "test_register",
        "password": password
    }
    # 步骤2：执行操作
    resp = api_session.post("/api/register", json=req_data)
    # 步骤3：精准断言（先断言状态码，再断言业务字段）
    assert resp.status_code == expected_code, f"状态码异常，预期{expected_code}，实际{resp.status_code}"
    if expected_code == 200:
        assert resp.json()["msg"] == "注册成功"
        assert "user_id" in resp.json()
    else:
        assert "密码" in resp.json()["msg"]  # 断言错误提示包含关键词
```

#### 2. 用例优化核心原则
- ❌ 禁止一个用例覆盖多个断言点（如同时测注册+登录+下单）；
- ✅ 用 `pytest.mark.parametrize` 替代重复用例（如多参数场景）；
- ✅ 断言优先校验「核心字段」（状态码 > 业务码 > 业务信息）；
- ✅ 禁止用例内写Fixture逻辑（如重复创建接口会话）；
- ✅ 测试数据放入 `tests/test_data/`（如JSON文件），避免硬编码：
  ```python
  # 读取测试数据文件示例
  import json
  def test_user_login(test_data_dir):
      with open(os.path.join(test_data_dir, "login_data.json"), "r") as f:
          login_data = json.load(f)
      resp = api_session.post("/api/login", json=login_data["valid"])
      assert resp.status_code == 200
  ```

### 四、自动化提效：CI/CD + 本地提效
#### 1. GitHub Actions 自动化（完整配置）
创建 `.github/workflows/pytest_ci.yml`，实现「提交/PR自动跑测试+覆盖率」：
```yaml
name: Pytest Auto Test

on:
  push:
    branches: [main, dev]  # 推送到主分支/开发分支触发
  pull_request:
    branches: [main]       # PR到主分支触发

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false  # 一个Python版本失败不影响其他版本
      matrix:
        python-version: ["3.8", "3.9", "3.10"]  # 多版本兼容测试

    steps:
      - name: 拉取代码
        uses: actions/checkout@v4

      - name: 设置Python环境
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"  # 缓存依赖，加速

      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 运行pytest（跳过标记为skip_ci的用例）
        run: |
          pytest --cov=src --cov-report=xml --cov-report=html -m "not skip_ci"

      - name: 上传覆盖率报告
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true  # 覆盖率不达标则CI失败

      - name: 上传HTML报告（供调试）
        uses: actions/upload-artifact@v4
        with:
          name: pytest-html-report-${{ matrix.python-version }}
          path: ./htmlcov
```

#### 2. 本地提效工具
- 安装 `pre-commit` 实现「提交前自动检查代码+跑冒烟用例」：
  1. 创建 `.pre-commit-config.yaml`：
     ```yaml
     repos:
       - repo: https://github.com/PyCQA/flake8
         rev: 6.0.0
         hooks:
           - id: flake8
             args: ["--config=.flake8"]
       - repo: local
         hooks:
           - id: pytest-smoke
             name: Run Smoke Tests
             entry: pytest -m smoke
             language: system
             pass_filenames: false
             always_run: true
     ```
  2. 安装并启用：
     ```bash
     pip install pre-commit
     pre-commit install
     ```
- 用 `pytest-xdist` 并行跑用例（本地提速50%+）：
  ```bash
  pytest -n auto  # auto：自动适配CPU核心数
  ```

### 五、协作规范：文档 + 模板
#### 1. README.md 核心内容（模板）
```markdown
# pytest_new
pytest 测试工程化示例/业务测试库

## 快速开始
### 1. 环境准备
​```bash
# 克隆仓库
git clone https://github.com/walkzzz/pytest_new.git
cd pytest_new
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
# 安装依赖
pip install -r requirements.txt
```

### 2. 运行测试
```bash
# 运行所有用例
pytest
# 仅运行冒烟用例
pytest -m smoke
# 运行指定文件
pytest tests/unit/test_user.py
# 并行运行+生成HTML报告
pytest -n auto --html=pytest-report.html
```

### 3. 目录结构
```
pytest_new/
├── .github/          # CI/CD配置
├── tests/            # 测试用例（unit/单元测试，integration/集成测试）
├── src/              # 被测试业务代码
├── docs/             # 测试文档（Fixture说明、用例设计）
├── pyproject.toml    # 项目配置
└── pytest.ini        # pytest配置
```

### 4. 核心规范
- 用例命名：test_业务场景_条件_预期结果
- Fixture作用域：session（全局）> module（模块）> function（用例）
- 断言原则：先状态码，后业务字段
```

#### 2. 新增 PR/Issue 模板（协作必备）
- 创建 `.github/ISSUE_TEMPLATE/bug_report.md`（bug反馈模板）：
  ```markdown
  ## 问题描述
  清晰描述测试用例/框架遇到的问题

  ## 复现步骤
  1. 运行命令：pytest xxx
  2. 执行操作：xxx
  3. 观察结果：xxx

  ## 预期结果
  xxx

  ## 实际结果
  xxx

  ## 环境信息
  - Python版本：
  - pytest版本：
  - 系统：
```
- 创建 `.github/PULL_REQUEST_TEMPLATE.md`（PR提交模板）：
  ```markdown
  ## 本次PR修改内容
  - [ ] 新增测试用例
  - [ ] 优化Fixture
  - [ ] 修复CI配置
  - [ ] 其他：xxx

  ## 测试验证
  - 本地运行pytest：✅/❌
  - 冒烟用例通过率：✅/❌
  - 覆盖率变化：xxx

  ## 备注
  xxx
  ```

### 六、落地优先级（按成本低/收益高排序）
1. 重构 `pyproject.toml` + `pytest.ini` + `.gitignore`（1小时完成）；
2. 标准化 `conftest.py` 的Fixture（2小时完成）；
3. 改造1-2个核心用例为规范示例（1小时完成）；
4. 配置GitHub Actions CI（1小时完成）；
5. 补充README和协作模板（1小时完成）；
6. 逐步推广到所有用例 + 接入pre-commit（按需）。

