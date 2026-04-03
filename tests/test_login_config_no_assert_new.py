import pytest

from src.pytest_runner import BaseTestCase


class TestLoginConfigNoAssertNew(BaseTestCase):
    config_filename = "configs/login_config_no_assert_new.yaml"
    project_name = "注册测试"

    def test_registration_flow_normal_registration(self):
        """注册流程测试 - normal_registration"""
        self.run_test_case("registration_flow", data_key="normal_registration")

    def test_registration_flow_invalid_nickname_empty(self):
        """注册流程测试 - invalid_nickname_empty"""
        self.run_test_case("registration_flow", data_key="invalid_nickname_empty")

    def test_registration_flow_invalid_password_short(self):
        """注册流程测试 - invalid_password_short"""
        self.run_test_case("registration_flow", data_key="invalid_password_short")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
