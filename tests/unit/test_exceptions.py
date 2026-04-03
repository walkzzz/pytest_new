import pytest


class TestExceptions:
    def test_base_error_inherits_from_exception(self):
        from src.exceptions import AutoTestBaseError

        assert issubclass(AutoTestBaseError, Exception)

    def test_app_start_error_inherits_from_base(self):
        from src.exceptions import AppStartError, AutoTestBaseError

        assert issubclass(AppStartError, AutoTestBaseError)

    def test_element_not_found_error_inherits_from_base(self):
        from src.exceptions import AutoTestBaseError, ElementNotFoundError

        assert issubclass(ElementNotFoundError, AutoTestBaseError)

    def test_step_execution_error_inherits_from_base(self):
        from src.exceptions import AutoTestBaseError, StepExecutionError

        assert issubclass(StepExecutionError, AutoTestBaseError)

    def test_configuration_error_inherits_from_base(self):
        from src.exceptions import AutoTestBaseError, ConfigurationError

        assert issubclass(ConfigurationError, AutoTestBaseError)

    def test_can_raise_and_catch_errors(self):
        from src.exceptions import ElementNotFoundError

        with pytest.raises(ElementNotFoundError):
            raise ElementNotFoundError("Element not found")

    def test_errors_can_contain_custom_message(self):
        from src.exceptions import AppStartError

        error = AppStartError("Failed to start app at path X")
        assert "Failed to start app" in str(error)
