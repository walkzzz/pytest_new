import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from pywinauto.application import WindowSpecification
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError

from pywinauto import keyboard, mouse

logger = logging.getLogger(__name__)


class BaseControl:
    """
    基础控件类 - 封装所有控件共有的操作

    功能：
    - 查找控件
    - 等待控件出现
    - 点击操作
    - 获取属性
    - 截图
    """

    def __init__(self, window: WindowSpecification, **locator):
        """
        初始化控件

        Args:
            window: 父窗口对象
            **locator: 控件定位参数，例如 title="确定", control_type="Button"
        """
        self.window = window
        self.locator = locator
        self.element = None
        self._find_element()

    def _find_element(self) -> bool:
        """
        内部方法：查找控件元素

        Returns:
            bool: 是否找到控件
        """
        try:
            self.element = self.window.child_window(**self.locator)
            return True
        except ElementNotFoundError:
            logger.warning(f"控件未找到: {self.locator}")
            return False

    def exists(self, timeout: int = 10) -> bool:
        """
        检查控件是否存在

        Args:
            timeout: 等待超时时间（秒）

        Returns:
            bool: 控件是否存在
        """
        try:
            if self.element:
                self.element.wait("exists", timeout=timeout)
                return True
            return self._find_element()
        except (TimeoutError, ElementNotFoundError):
            return False

    def wait(self, state: str = "exists", timeout: int = 10, retry_interval: float = 0.5) -> bool:
        """
        等待控件达到指定状态

        Args:
            state: 等待状态 ('exists', 'visible', 'enabled', 'ready')
            timeout: 超时时间（秒）
            retry_interval: 重试间隔（秒）

        Returns:
            bool: 是否成功等待到指定状态
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if self._find_element():
                    self.element.wait(state, timeout=1)
                    logger.debug(f"控件达到状态 '{state}': {self.locator}")
                    return True
            except (TimeoutError, ElementNotFoundError):
                pass
            time.sleep(retry_interval)

        logger.error(f"等待控件状态 '{state}' 超时: {self.locator}")
        return False

    def wait_visible(self, timeout: int = 10) -> bool:
        """等待控件可见"""
        return self.wait("visible", timeout)

    def wait_enabled(self, timeout: int = 10) -> bool:
        """等待控件可用"""
        return self.wait("enabled", timeout)

    def click(self, use_input: bool = False, timeout: int = 10) -> bool:
        """
        点击控件

        Args:
            use_input: 是否使用 click_input()（模拟真实鼠标点击）
            timeout: 等待控件可用的超时时间

        Returns:
            bool: 是否成功点击
        """
        try:
            if not self.wait_enabled(timeout):
                logger.error(f"控件不可点击: {self.locator}")
                return False

            self.set_focus()

            if use_input:
                self.element.click_input()
            else:
                self.element.click()

            logger.info(f"点击控件成功: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"点击控件失败: {self.locator}, 错误: {e}")
            return False

    def double_click(self, use_input: bool = False, timeout: int = 10) -> bool:
        """双击控件"""
        try:
            if not self.wait_enabled(timeout):
                return False

            if use_input:
                self.element.double_click_input()
            else:
                self.element.double_click()

            logger.info(f"双击控件成功: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"双击控件失败: {self.locator}, 错误: {e}")
            return False

    def right_click(self, use_input: bool = False, timeout: int = 10) -> bool:
        """右键点击控件"""
        try:
            if not self.wait_enabled(timeout):
                return False

            if use_input:
                self.element.right_click_input()
            else:
                self.element.right_click()

            logger.info(f"右键点击控件成功: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"右键点击控件失败: {self.locator}, 错误: {e}")
            return False

    def get_property(self, property_name: str) -> Any:
        """
        获取控件属性

        Args:
            property_name: 属性名称

        Returns:
            属性值，失败返回 None
        """
        try:
            if not self._find_element():
                return None

            value = getattr(self.element, property_name, None)
            if callable(value):
                value = value()
            logger.debug(f"获取控件属性 {property_name}: {value}")
            return value
        except Exception as e:
            logger.error(f"获取控件属性失败 {property_name}: {e}")
            return None

    def set_focus(self) -> bool:
        """设置控件焦点"""
        try:
            if not self._find_element():
                return False

            self.element.set_focus()
            logger.debug(f"设置控件焦点成功: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"设置控件焦点失败: {e}")
            return False

    def get_rectangle(self) -> Optional[Tuple[int, int, int, int]]:
        """
        获取控件矩形区域

        Returns:
            (left, top, right, bottom) 或 None
        """
        try:
            if not self._find_element():
                return None

            rect = self.element.rectangle()
            return (rect.left, rect.top, rect.right, rect.bottom)
        except Exception as e:
            logger.error(f"获取控件矩形失败: {e}")
            return None

    def capture_as_image(self, file_path: Optional[str] = None):
        """
        截图控件

        Args:
            file_path: 保存路径（可选）

        Returns:
            PIL.Image 对象或 None
        """
        try:
            if not self._find_element():
                return None

            image = self.element.capture_as_image()

            if file_path:
                image.save(file_path)
                logger.info(f"控件截图保存成功: {file_path}")

            return image
        except Exception as e:
            logger.error(f"控件截图失败: {e}")
            return None

    def is_visible(self) -> bool:
        """检查控件是否可见"""
        try:
            if not self._find_element():
                return False
            return self.element.is_visible()
        except Exception:
            return False

    def is_enabled(self) -> bool:
        """检查控件是否可用"""
        try:
            if not self._find_element():
                return False
            return self.element.is_enabled()
        except Exception:
            return False

    def get_control_type(self) -> Optional[str]:
        """获取控件类型"""
        elem_info = self.get_property("element_info")
        return elem_info.control_type if elem_info else None
