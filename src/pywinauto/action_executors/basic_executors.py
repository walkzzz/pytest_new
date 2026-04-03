import logging
from typing import Optional

from src.pywinauto.controls import (
    ButtonControl,
    ComboBoxControl,
    EditControl,
    ImageControl,
    ListBoxControl,
    TabControl,
)

from .base_executor import BaseExecutor

logger = logging.getLogger(__name__)


class ButtonExecutor(BaseExecutor):
    """
    按钮执行器 - 封装按钮特有操作
    """

    def __init__(self, control: ButtonControl):
        super().__init__(control)
        self.control = control

    def is_checked(self) -> Optional[bool]:
        """检查按钮是否被选中"""
        return self.control.is_checked()

    def check(self) -> bool:
        """选中按钮"""
        logger.info(f"按钮执行器: 选中按钮 {self.control.locator}")
        return self.control.check()

    def uncheck(self) -> bool:
        """取消选中"""
        logger.info(f"按钮执行器: 取消选中按钮 {self.control.locator}")
        return self.control.uncheck()


class EditExecutor(BaseExecutor):
    """
    输入框执行器 - 封装输入框特有操作
    """

    def __init__(self, control: EditControl):
        super().__init__(control)
        self.control = control

    def set_text(self, text: str, clear_first: bool = True, timeout: int = 10) -> bool:
        """设置文本"""
        logger.info(f"输入框执行器: 设置文本 '{text}' -> {self.control.locator}")
        return self.control.set_text(text, clear_first, timeout)

    def get_text(self) -> Optional[str]:
        """获取文本"""
        return self.control.get_text()

    def clear_text(self) -> bool:
        """清空文本"""
        logger.info(f"输入框执行器: 清空文本 {self.control.locator}")
        return self.control.clear_text()

    def type_text(self, text: str, with_spaces: bool = True, pause: float = 0.0) -> bool:
        """模拟键盘逐字符输入"""
        logger.info(f"输入框执行器: 键盘输入文本 '{text}'")
        return self.control.type_text(text, with_spaces, pause)

    def is_editable(self) -> bool:
        """检查是否可编辑"""
        return self.control.is_editable()


class ComboBoxExecutor(BaseExecutor):
    """
    下拉框执行器 - 封装下拉框特有操作
    """

    def __init__(self, control: ComboBoxControl):
        super().__init__(control)
        self.control = control

    def select(self, item: str, timeout: int = 10) -> bool:
        """选择下拉框项"""
        logger.info(f"下拉框执行器: 选择项 '{item}'")
        return self.control.select(item, timeout)

    def select_by_index(self, index: int, timeout: int = 10) -> bool:
        """按索引选择下拉框项"""
        logger.info(f"下拉框执行器: 按索引选择项 {index}")
        return self.control.select_by_index(index, timeout)

    def get_items(self) -> list:
        """获取所有下拉框选项"""
        return self.control.get_items()

    def get_selected_item(self) -> Optional[str]:
        """获取当前选中项"""
        return self.control.get_selected_item()


class ListBoxExecutor(BaseExecutor):
    """
    列表框执行器 - 封装列表框特有操作
    """

    def __init__(self, control: ListBoxControl):
        super().__init__(control)
        self.control = control

    def select(self, item: str, timeout: int = 10) -> bool:
        """选择列表项"""
        logger.info(f"列表框执行器: 选择项 '{item}'")
        return self.control.select(item, timeout)

    def select_by_index(self, index: int, timeout: int = 10) -> bool:
        """按索引选择列表项"""
        logger.info(f"列表框执行器: 按索引选择项 {index}")
        return self.control.select_by_index(index, timeout)

    def get_items(self) -> list:
        """获取所有列表项"""
        return self.control.get_items()

    def get_selected_items(self) -> list:
        """获取选中的列表项"""
        return self.control.get_selected_items()


class TabExecutor(BaseExecutor):
    """
    标签页执行器 - 封装标签页特有操作
    """

    def __init__(self, control: TabControl):
        super().__init__(control)
        self.control = control

    def select_tab(self, tab_name: str, timeout: int = 10) -> bool:
        """选择标签页"""
        logger.info(f"标签页执行器: 选择标签页 '{tab_name}'")
        return self.control.select_tab(tab_name, timeout)

    def select_tab_by_index(self, index: int, timeout: int = 10) -> bool:
        """按索引选择标签页"""
        logger.info(f"标签页执行器: 按索引选择标签页 {index}")
        return self.control.select_tab_by_index(index, timeout)

    def get_tabs(self) -> list:
        """获取所有标签页名称"""
        return self.control.get_tabs()

    def get_selected_tab(self) -> Optional[str]:
        """获取当前选中标签页"""
        return self.control.get_selected_tab()


class ImageExecutor(BaseExecutor):
    """
    图片执行器 - 封装图片特有操作
    """

    def __init__(self, control: ImageControl):
        super().__init__(control)
        self.control = control

    def click_input(self, timeout: int = 10) -> bool:
        """
        模拟真实鼠标点击图片控件

        Args:
            timeout: 等待控件可用的超时时间

        Returns:
            bool: 是否成功点击
        """
        logger.info(f"图片执行器: 模拟鼠标点击 {self.control.locator}")
        return self.control.click_input(timeout)

    def capture_as_image(self, file_path: Optional[str] = None):
        """截图图片控件"""
        return self.control.capture_as_image(file_path)

    def get_image_size(self) -> Optional[tuple]:
        """获取图片尺寸"""
        return self.control.get_image_size()
