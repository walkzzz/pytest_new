import time
import logging
from functools import wraps
from typing import Any, Callable, Optional
from src.exceptions import ElementNotFoundError

logger = logging.getLogger(__name__)


def wait_until_visible(elem: Any, timeout: int = 10, retry_interval: float = 0.5) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if elem.is_visible():
                return True
        except Exception:
            pass
        time.sleep(retry_interval)
    raise ElementNotFoundError(f"元素超时 {timeout} 秒仍未可见")


def wait_until_enabled(elem: Any, timeout: int = 10, retry_interval: float = 0.5) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if elem.is_enabled():
                return True
        except Exception:
            pass
        time.sleep(retry_interval)
    raise ElementNotFoundError(f"元素超时 {timeout} 秒仍未可用")


def wait_until_exists(elem: Any, timeout: int = 10, retry_interval: float = 0.5) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if elem.exists():
                return True
        except Exception:
            pass
        time.sleep(retry_interval)
    raise ElementNotFoundError(f"元素超时 {timeout} 秒仍未存在")


def with_retry(func: Optional[Callable] = None, retry_times: int = 2, delay: float = 0.5, exceptions: tuple = (Exception,)):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exception = Exception("重试次数耗尽")
            for i in range(retry_times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if i < retry_times:
                        logger.warning(f"{fn.__name__} 失败 (尝试 {i+1}/{retry_times+1}): {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"{fn.__name__} 最终失败: {e}")
            raise last_exception
        return wrapper
    
    if func is None:
        return decorator
    return decorator(func)
