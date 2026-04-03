from src.pywinauto.controls import (
    BaseControl,
    ButtonControl,
    ComboBoxControl,
    EditControl,
    ImageControl,
    ListBoxControl,
    TabControl,
)

from .base_assertion import BaseAssertion
from .basic_assertions import (
    ButtonAssertion,
    ComboBoxAssertion,
    EditAssertion,
    ImageAssertion,
    ListBoxAssertion,
    TabAssertion,
)


class AssertionFactory:
    """
    断言工厂：根据控件类型自动创建对应断言实例
    与控件工厂、动作执行器工厂完美配套
    """

    @staticmethod
    def get_assertion(control: BaseControl) -> BaseAssertion:
        """
        自动匹配断言类
        Args:
            control: 控件实例
        Returns:
            对应控件的断言实例
        """
        if isinstance(control, ButtonControl):
            return ButtonAssertion(control)
        elif isinstance(control, EditControl):
            return EditAssertion(control)
        elif isinstance(control, ComboBoxControl):
            return ComboBoxAssertion(control)
        elif isinstance(control, ListBoxControl):
            return ListBoxAssertion(control)
        elif isinstance(control, TabControl):
            return TabAssertion(control)
        elif isinstance(control, ImageControl):
            return ImageAssertion(control)
        else:
            return BaseAssertion(control)
