"""
测试用例最佳实践示例
遵循「test_业务场景_条件_预期结果」命名规范
"""

import json
import os

import pytest


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.parametrize(
    "username, password, expected_result",
    [
        ("test_user", "secure_password_123", "登录成功"),
        ("", "secure_password_123", "用户名不能为空"),
        ("test_user", "123", "密码长度至少6位"),
    ],
    ids=["有效用户名密码", "空用户名", "密码过短"],
)
def test_user_login_credentials_validation(test_data_dir, username, password, expected_result):
    """测试用户登录-凭据验证（最佳实践示例）"""
    # 步骤1：读取测试数据文件（避免硬编码）
    with open(os.path.join(test_data_dir, "login_data.json"), "r", encoding="utf-8") as f:
        test_data = json.load(f)  # noqa: F841

    # 步骤2：构造请求数据（实际项目中可能是UI操作）
    login_data = {"username": username, "password": password}

    # 步骤3：执行操作（这里模拟UI登录操作）
    # 实际项目中可能是：app.login(login_data)
    print(f"执行登录操作: {login_data}")

    # 步骤4：模拟验证结果（实际项目中从UI获取结果）
    if username == "test_user" and password == "secure_password_123":
        actual_result = "登录成功"
    elif not username:
        actual_result = "用户名不能为空"
    elif len(password) < 6:
        actual_result = "密码长度至少6位"
    else:
        actual_result = "登录失败"

    # 步骤5：精准断言（优先核心业务字段）
    assert actual_result == expected_result, f"登录验证失败: 预期'{expected_result}'，实际'{actual_result}'"

    # 附加断言（如有必要）
    # 这里可以根据实际业务需求添加更多断言


@pytest.mark.ui
@pytest.mark.regression
class TestUserRegistration:
    """用户注册测试类（类形式的测试用例）"""

    @pytest.fixture(autouse=True)
    def setup_method(self, temp_test_data):
        """每个测试方法的前置操作"""
        self.test_data_file = temp_test_data
        with open(self.test_data_file, "r", encoding="utf-8") as f:
            self.test_data = json.load(f)
        yield
        # 后置操作（自动执行）

    def test_user_registration_valid_data_creates_account(self):
        """测试用户注册-有效数据创建账户"""
        # 使用Fixture中的测试数据
        test_id = self.test_data["test_id"]

        # 模拟注册操作
        print(f"测试ID: {test_id}")
        registration_success = True

        # 断言
        assert registration_success, "注册应该成功"
        assert test_id is not None, "测试ID应该存在"

    def test_user_registration_backend_compatibility(self, backend_type):
        """测试用户注册-后端兼容性（参数化Fixture示例）"""
        # backend_type来自conftest.py中的参数化Fixture
        print(f"测试后端类型: {backend_type}")

        # 模拟不同后端的注册操作
        if backend_type == "uia":
            assert True, "uia后端应支持"
        else:
            assert True, "win32后端应支持"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
