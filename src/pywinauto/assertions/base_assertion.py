import logging
from typing import Any
from src.pywinauto.controls import BaseControl

logger = logging.getLogger(__name__)


class ControlAssertionError(Exception):
    """控件断言失败异常"""

    pass


class BaseAssertion:
    """
    控件断言基类
    封装所有控件通用的断言逻辑，所有专属断言类的父类
    """

    def __init__(self, control: BaseControl):
        self.control = control
        self.locator = control.locator
        self.control_name = control.__class__.__name__

    def assert_exists(self, timeout: int = 10) -> None:
        """断言：控件存在"""
        if not self.control.exists(timeout):
            raise ControlAssertionError(
                f"【断言失败】{self.control_name} 不存在 | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】{self.control_name} 存在 | 定位: {self.locator}")

    def assert_not_exists(self, timeout: int = 10) -> None:
        """断言：控件不存在"""
        if self.control.exists(timeout):
            raise ControlAssertionError(
                f"【断言失败】{self.control_name} 仍存在 | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】{self.control_name} 不存在 | 定位: {self.locator}")

    def assert_visible(self) -> None:
        """断言：控件可见"""
        if not self.control.is_visible():
            raise ControlAssertionError(
                f"【断言失败】{self.control_name} 不可见 | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】{self.control_name} 可见 | 定位: {self.locator}")

    def assert_enabled(self) -> None:
        """断言：控件可用（可点击/可操作）"""
        if not self.control.is_enabled():
            raise ControlAssertionError(
                f"【断言失败】{self.control_name} 不可用 | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】{self.control_name} 可用 | 定位: {self.locator}")

    def assert_disabled(self) -> None:
        """断言：控件禁用"""
        if self.control.is_enabled():
            raise ControlAssertionError(
                f"【断言失败】{self.control_name} 未禁用 | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】{self.control_name} 禁用 | 定位: {self.locator}")

    def assert_property_equal(self, prop_name: str, expected: Any) -> None:
        """断言：控件属性等于预期值"""
        actual = self.control.get_property(prop_name)
        if actual != expected:
            raise ControlAssertionError(
                f"【断言失败】属性 {prop_name} 不匹配 | 预期: {expected} | 实际: {actual} | 定位: {self.locator}"
            )
        logger.info(
            f"【断言成功】属性 {prop_name} 匹配 | 值: {expected} | 定位: {self.locator}"
        )

    def assert_rect_valid(self) -> None:
        """断言：控件矩形区域有效（非空）"""
        rect = self.control.get_rectangle()
        if rect is None:
            raise ControlAssertionError(
                f"【断言失败】控件矩形区域无效 | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】控件矩形区域有效 | 定位: {self.locator}")
