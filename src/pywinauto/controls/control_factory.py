from pywinauto.application import WindowSpecification

from .advanced_controls import CalendarControl, ProgressBarControl, SliderControl, StatusBarControl, TreeControl
from .base_control import BaseControl
from .basic_controls import ButtonControl, ComboBoxControl, EditControl, ListBoxControl, TabControl
from .complex_controls import (
    DialogControl,
    GroupBoxControl,
    HyperlinkControl,
    ImageControl,
    LabelControl,
    MenuControl,
    RichEditControl,
    ScrollBarControl,
    ToolbarControl,
)


class ControlFactory:
    """
    控件工厂类 - 简化所有控件的创建
    """

    def __init__(self, window: WindowSpecification):
        self.window = window

    def button(self, **locator) -> ButtonControl:
        """创建按钮控件"""
        return ButtonControl(self.window, **locator)

    def edit(self, **locator) -> EditControl:
        """创建文本输入控件"""
        return EditControl(self.window, **locator)

    def combobox(self, **locator) -> ComboBoxControl:
        """创建下拉框控件"""
        return ComboBoxControl(self.window, **locator)

    def listbox(self, **locator) -> ListBoxControl:
        """创建列表框控件"""
        return ListBoxControl(self.window, **locator)

    def tab(self, **locator) -> TabControl:
        """创建标签页控件"""
        return TabControl(self.window, **locator)

    def tree(self, **locator) -> TreeControl:
        """创建树形控件"""
        return TreeControl(self.window, **locator)

    def progressbar(self, **locator) -> ProgressBarControl:
        """创建进度条控件"""
        return ProgressBarControl(self.window, **locator)

    def slider(self, **locator) -> SliderControl:
        """创建滑块控件"""
        return SliderControl(self.window, **locator)

    def calendar(self, **locator) -> CalendarControl:
        """创建日历控件"""
        return CalendarControl(self.window, **locator)

    def statusbar(self, **locator) -> StatusBarControl:
        """创建状态栏控件"""
        return StatusBarControl(self.window, **locator)

    def menu(self, **locator) -> MenuControl:
        """创建菜单控件"""
        return MenuControl(self.window, **locator)

    def toolbar(self, **locator) -> ToolbarControl:
        """创建工具栏控件"""
        return ToolbarControl(self.window, **locator)

    def hyperlink(self, **locator) -> HyperlinkControl:
        """创建超链接控件"""
        return HyperlinkControl(self.window, **locator)

    def groupbox(self, **locator) -> GroupBoxControl:
        """创建分组框控件"""
        return GroupBoxControl(self.window, **locator)

    def scrollbar(self, **locator) -> ScrollBarControl:
        """创建滚动条控件"""
        return ScrollBarControl(self.window, **locator)

    def richedit(self, **locator) -> RichEditControl:
        """创建富文本控件"""
        return RichEditControl(self.window, **locator)

    def label(self, **locator) -> LabelControl:
        """创建标签控件"""
        return LabelControl(self.window, **locator)

    def dialog(self, **locator) -> DialogControl:
        """创建对话框控件"""
        return DialogControl(self.window, **locator)

    def image(self, **locator) -> ImageControl:
        """创建图片控件"""
        return ImageControl(self.window, **locator)

    def base(self, **locator) -> BaseControl:
        """创建基础控件"""
        return BaseControl(self.window, **locator)
