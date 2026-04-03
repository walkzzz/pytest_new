from src.pywinauto.controls import (
    BaseControl,
    ButtonControl,
    ControlFactory,
    EditControl,
    ImageControl,
)

from .base_executor import BaseExecutor
from .basic_executors import ButtonExecutor, EditExecutor, ImageExecutor


class ActionExecutorFactory:
    """
    执行器工厂类 - 简化所有执行器的创建
    """

    def __init__(self, control_factory: ControlFactory):
        self.control_factory = control_factory

    def base(self, **locator) -> BaseExecutor:
        """创建基础执行器"""
        control = self.control_factory.base(**locator)
        return BaseExecutor(control)

    def button(self, **locator) -> ButtonExecutor:
        """创建按钮执行器"""
        control = self.control_factory.button(**locator)
        return ButtonExecutor(control)

    def edit(self, **locator) -> EditExecutor:
        """创建输入框执行器"""
        control = self.control_factory.edit(**locator)
        return EditExecutor(control)

    def image(self, **locator) -> ImageExecutor:
        """创建图片执行器"""
        control = self.control_factory.image(**locator)
        return ImageExecutor(control)
