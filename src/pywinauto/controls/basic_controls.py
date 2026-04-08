import logging
from typing import Optional

from pywinauto.application import WindowSpecification

from .base_control import BaseControl

logger = logging.getLogger(__name__)


class ButtonControl(BaseControl):
    """
    按钮控件 - 封装按钮特有操作
    适用于：Button, CheckBox, RadioButton
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def is_checked(self) -> Optional[bool]:
        """检查按钮是否被选中（CheckBox/RadioButton）"""
        try:
            if not self._find_element():
                return None
            assert self.element is not None
            return self.element.get_toggle_state() == 1
        except Exception as e:
            logger.error(f"检查按钮选中状态失败: {e}")
            return None

    def check(self) -> bool:
        """选中按钮（CheckBox/RadioButton）"""
        try:
            if not self.is_checked():
                self.click()
                logger.info(f"选中按钮: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"选中按钮失败: {e}")
            return False

    def uncheck(self) -> bool:
        """取消选中（CheckBox）"""
        try:
            if self.is_checked():
                self.click()
                logger.info(f"取消选中按钮: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"取消选中按钮失败: {e}")
            return False


class EditControl(BaseControl):
    """
    文本输入控件 - 封装输入框特有操作
    适用于：Edit, TextBox
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def set_text(self, text: str, clear_first: bool = True, timeout: int = 10) -> bool:
        """设置文本"""
        try:
            if not self.wait_enabled(timeout):
                return False
            assert self.element is not None

            if clear_first:
                self.element.set_text("")

            self.element.set_text(text)
            logger.info(f"设置文本成功: '{text}' -> {self.locator}")
            return True
        except Exception as e:
            logger.error(f"设置文本失败: {e}")
            return False

    def get_text(self) -> Optional[str]:
        """获取文本"""
        try:
            if not self._find_element():
                return None
            assert self.element is not None
            text = self.element.get_value()
            logger.debug(f"获取文本: '{text}'")
            return text
        except Exception as e:
            logger.error(f"获取文本失败: {e}")
            return None

    def clear_text(self) -> bool:
        """清空文本"""
        return self.set_text("", clear_first=False)

    def type_text(
        self, text: str, with_spaces: bool = True, pause: float = 0.0
    ) -> bool:
        """模拟键盘逐字符输入"""
        try:
            if not self.wait_enabled():
                return False

            self.set_focus()
            assert self.element is not None
            self.element.type_keys(text, with_spaces=with_spaces, pause=pause)
            logger.info(f"键盘输入文本成功: '{text}'")
            return True
        except Exception as e:
            logger.error(f"键盘输入文本失败: {e}")
            return False

    def is_editable(self) -> bool:
        """检查是否可编辑"""
        try:
            if not self._find_element():
                return False
            assert self.element is not None
            return self.element.is_editable()
        except Exception:
            return False


class ComboBoxControl(BaseControl):
    """
    下拉框控件 - 封装下拉框特有操作
    适用于：ComboBox
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def select(self, item: str, timeout: int = 10) -> bool:
        """选择下拉框项（按文本）"""
        try:
            if not self.wait_enabled(timeout):
                return False
            assert self.element is not None
            self.element.select(item)
            logger.info(f"选择下拉框项: '{item}'")
            return True
        except Exception as e:
            logger.error(f"选择下拉框项失败: {e}")
            return False

    def select_by_index(self, index: int, timeout: int = 10) -> bool:
        """按索引选择下拉框项"""
        try:
            if not self.wait_enabled(timeout):
                return False

            items = self.get_items()
            if 0 <= index < len(items):
                return self.select(items[index])
            logger.error(f"索引超出范围: {index}, 总项数: {len(items)}")
            return False
        except Exception as e:
            logger.error(f"按索引选择失败: {e}")
            return False

    def get_items(self) -> list:
        """获取所有下拉框选项"""
        try:
            if not self._find_element():
                return []
            assert self.element is not None
            items = self.element.get_items()
            logger.debug(f"下拉框选项: {items}")
            return items
        except Exception as e:
            logger.error(f"获取下拉框选项失败: {e}")
            return []

    def get_selected_item(self) -> Optional[str]:
        """获取当前选中项"""
        try:
            if not self._find_element():
                return None
            assert self.element is not None
            selected = self.element.selected_text()
            logger.debug(f"当前选中项: {selected}")
            return selected
        except Exception as e:
            logger.error(f"获取选中项失败: {e}")
            return None


class ListBoxControl(BaseControl):
    """
    列表框控件 - 封装列表框特有操作
    适用于：ListBox, ListView
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def select(self, item: str, timeout: int = 10) -> bool:
        """选择列表项（按文本）"""
        try:
            if not self.wait_enabled(timeout):
                return False
            assert self.element is not None
            self.element.select(item)
            logger.info(f"选择列表项: '{item}'")
            return True
        except Exception as e:
            logger.error(f"选择列表项失败: {e}")
            return False

    def select_by_index(self, index: int, timeout: int = 10) -> bool:
        """按索引选择列表项"""
        try:
            if not self.wait_enabled(timeout):
                return False
            assert self.element is not None
            items = self.get_items()
            if 0 <= index < len(items):
                self.element.select(items[index])
                return True
            logger.error(f"索引超出范围: {index}")
            return False
        except Exception as e:
            logger.error(f"按索引选择列表项失败: {e}")
            return False

    def get_items(self) -> list:
        """获取所有列表项"""
        try:
            if not self._find_element():
                return []
            assert self.element is not None
            items = self.element.get_items()
            logger.debug(f"列表项: {items}")
            return items
        except Exception as e:
            logger.error(f"获取列表项失败: {e}")
            return []

    def get_selected_items(self) -> list:
        """获取选中的列表项"""
        try:
            if not self._find_element():
                return []
            assert self.element is not None
            selected = self.element.get_selected_items()
            logger.debug(f"选中项: {selected}")
            return selected
        except Exception as e:
            logger.error(f"获取选中项失败: {e}")
            return []


class TabControl(BaseControl):
    """
    标签页控件 - 封装标签页特有操作
    适用于：TabControl
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def select_tab(self, tab_name: str, timeout: int = 10) -> bool:
        """选择标签页（按名称）"""
        try:
            if not self.wait_enabled(timeout):
                return False
            assert self.element is not None
            self.element.select(tab_name)
            logger.info(f"选择标签页: '{tab_name}'")
            return True
        except Exception as e:
            logger.error(f"选择标签页失败: {e}")
            return False

    def select_tab_by_index(self, index: int, timeout: int = 10) -> bool:
        """按索引选择标签页"""
        try:
            if not self.wait_enabled(timeout):
                return False
            assert self.element is not None
            tabs = self.get_tabs()
            if 0 <= index < len(tabs):
                return self.select_tab(tabs[index])
            logger.error(f"标签页索引超出范围: {index}")
            return False
        except Exception as e:
            logger.error(f"按索引选择标签页失败: {e}")
            return False

    def get_tabs(self) -> list:
        """获取所有标签页名称"""
        try:
            if not self._find_element():
                return []
            assert self.element is not None
            tabs = self.element.get_items()
            logger.debug(f"标签页列表: {tabs}")
            return tabs
        except Exception as e:
            logger.error(f"获取标签页失败: {e}")
            return []

    def get_selected_tab(self) -> Optional[str]:
        """获取当前选中标签页"""
        try:
            if not self._find_element():
                return None
            assert self.element is not None
            selected = self.element.get_selected_tab()
            logger.debug(f"当前标签页: {selected}")
            return selected
        except Exception as e:
            logger.error(f"获取当前标签页失败: {e}")
            return None
