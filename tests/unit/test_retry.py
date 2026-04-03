import pytest
import time
from unittest.mock import patch, MagicMock


class TestRetry:
    def test_retry_success_first_attempt(self):
        from src.utils.retry import retry

        @retry(max_attempts=3, delay=0.1)
        def success_func():
            return "success"

        result = success_func()
        assert result == "success"

    def test_retry_success_after_failures(self):
        from src.utils.retry import retry

        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("fail")
            return "success"

        result = flaky_func()
        assert result == "success"
        assert call_count == 2

    def test_retry_max_attempts_exceeded(self):
        from src.utils.retry import retry

        @retry(max_attempts=3, delay=0.1)
        def always_fail():
            raise ValueError("always fail")

        with pytest.raises(ValueError, match="always fail"):
            always_fail()

    def test_retry_with_custom_exception(self):
        from src.utils.retry import retry

        @retry(max_attempts=2, delay=0.1, exceptions=(ValueError,))
        def only_value_error():
            raise TypeError("not caught")

        with pytest.raises(TypeError, match="not caught"):
            only_value_error()
