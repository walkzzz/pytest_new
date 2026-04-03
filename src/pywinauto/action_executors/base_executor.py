import logging
from typing import Any

from src.pywinauto.controls import BaseControl

logger = logging.getLogger(__name__)


class BaseExecutor:
    """
    基础执行器 - 封装对控件的通用操作执行
    """

    def __init__(self, control: BaseControl):
        self.control = control

    def wait_visible(self, timeout: int = 10) -> bool:
        """等待控件可见"""
        logger.debug(f"执行器: 等待控件可见 {self.control.locator}")
        return self.control.wait_visible(timeout)

    def wait_enabled(self, timeout: int = 10) -> bool:
        """等待控件可用"""
        logger.debug(f"执行器: 等待控件可用 {self.control.locator}")
        return self.control.wait_enabled(timeout)

    def click(self, use_input: bool = False, timeout: int = 10) -> bool:
        """点击控件"""
        logger.info(f"执行器: 点击控件 {self.control.locator}")
        return self.control.click(use_input, timeout)

    def double_click(self, use_input: bool = False, timeout: int = 10) -> bool:
        """双击控件"""
        logger.info(f"执行器: 双击控件 {self.control.locator}")
        return self.control.double_click(use_input, timeout)

    def right_click(self, use_input: bool = False, timeout: int = 10) -> bool:
        """右键点击控件"""
        logger.info(f"执行器: 右键点击控件 {self.control.locator}")
        return self.control.right_click(use_input, timeout)

    def get_property(self, property_name: str) -> Any:
        """获取控件属性"""
        return self.control.get_property(property_name)

    def set_focus(self) -> bool:
        """设置控件焦点"""
        return self.control.set_focus()

    def is_visible(self) -> bool:
        """检查控件是否可见"""
        return self.control.is_visible()

    def is_enabled(self) -> bool:
        """检查控件是否可用"""
        return self.control.is_enabled()
