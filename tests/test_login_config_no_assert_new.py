import pytest
from src.pytest_runner import BaseTestCase


class TestRegistrationFlow(BaseTestCase):
    config_filename = "configs/login_config_no_assert_new.yaml"
    project_name = "注册测试"

    @pytest.mark.smoke
    def test_registration_with_valid_data(self):
        """正常注册流程 - 验证完整注册功能"""
        self.run_test_case("registration_flow", data_key="normal_registration")

    @pytest.mark.regression
    def test_registration_with_empty_nickname(self):
        """负向测试 - 空昵称应该注册失败"""
        self.run_test_case("registration_flow", data_key="invalid_nickname_empty")

    @pytest.mark.regression
    def test_registration_with_short_password(self):
        """负向测试 - 短密码应该注册失败"""
        self.run_test_case("registration_flow", data_key="invalid_password_short")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
