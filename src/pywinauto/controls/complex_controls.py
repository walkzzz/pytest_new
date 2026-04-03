import logging
import time
from typing import List, Optional

from pywinauto.application import WindowSpecification

from .base_control import BaseControl
from .basic_controls import ButtonControl

logger = logging.getLogger(__name__)


class MenuControl(BaseControl):
    """
    菜单控件 - 封装Menu/MenuItem特有操作
    适用于：Menu, MenuItem
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def click_menu_item(self, path: List[str], timeout: int = 10) -> bool:
        """
        点击菜单项（支持多级菜单）
        Example: click_menu_item(["文件", "新建", "文本文档"])
        """
        try:
            if not self.wait_enabled(timeout):
                return False

            self.element.click_input()
            for item in path:
                time.sleep(0.2)
                menu_item = self.window.child_window(title=item, control_type="MenuItem")
                menu_item.click_input()

            logger.info(f"点击菜单项: {' -> '.join(path)}")
            return True
        except Exception as e:
            logger.error(f"点击菜单项失败: {e}")
            return False

    def get_menu_items(self) -> list:
        """获取一级菜单项"""
        try:
            if not self._find_element():
                return []

            items = self.element.get_items()
            logger.debug(f"菜单项列表: {items}")
            return items
        except Exception as e:
            logger.error(f"获取菜单项失败: {e}")
            return []

    def is_menu_item_enabled(self, item: str) -> bool:
        """检查菜单项是否可用"""
        try:
            if not self._find_element():
                return False

            menu_item = self.window.child_window(title=item, control_type="MenuItem")
            return menu_item.is_enabled()
        except Exception as e:
            logger.error(f"检查菜单项状态失败: {e}")
            return False


class ToolbarControl(BaseControl):
    """
    工具栏控件 - 封装Toolbar特有操作
    适用于：Toolbar
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def click_button(self, button_name: str, timeout: int = 10) -> bool:
        """点击工具栏按钮（按名称）"""
        try:
            if not self.wait_enabled(timeout):
                return False

            self.element.click_button(button_name)
            logger.info(f"点击工具栏按钮: {button_name}")
            return True
        except Exception as e:
            logger.error(f"点击工具栏按钮失败: {e}")
            return False

    def click_button_by_index(self, index: int, timeout: int = 10) -> bool:
        """按索引点击工具栏按钮"""
        try:
            if not self.wait_enabled(timeout):
                return False

            self.element.click_button(index=index)
            logger.info(f"点击工具栏按钮（索引{index}）")
            return True
        except Exception as e:
            logger.error(f"按索引点击工具栏按钮失败: {e}")
            return False

    def get_buttons(self) -> list:
        """获取所有工具栏按钮文本"""
        try:
            if not self._find_element():
                return []

            buttons = self.element.button_names()
            logger.debug(f"工具栏按钮列表: {buttons}")
            return buttons
        except Exception as e:
            logger.error(f"获取工具栏按钮失败: {e}")
            return []


class HyperlinkControl(BaseControl):
    """
    超链接控件 - 封装Hyperlink特有操作
    适用于：Hyperlink
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def get_link_text(self) -> Optional[str]:
        """获取超链接文本"""
        try:
            if not self._find_element():
                return None

            text = self.element.window_text()
            logger.debug(f"超链接文本: {text}")
            return text
        except Exception as e:
            logger.error(f"获取超链接文本失败: {e}")
            return None

    def get_link_url(self) -> Optional[str]:
        """获取超链接URL"""
        try:
            if not self._find_element():
                return None

            url = self.element.get_property("NavigateUrl")
            logger.debug(f"超链接URL: {url}")
            return url
        except Exception as e:
            logger.error(f"获取超链接URL失败: {e}")
            return None


class GroupBoxControl(BaseControl):
    """
    分组框控件 - 封装GroupBox特有操作
    适用于：GroupBox
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def get_group_text(self) -> Optional[str]:
        """获取分组框标题"""
        try:
            if not self._find_element():
                return None

            text = self.element.window_text()
            logger.debug(f"分组框标题: {text}")
            return text
        except Exception as e:
            logger.error(f"获取分组框标题失败: {e}")
            return None

    def get_children_controls(self) -> list:
        """获取分组框内所有子控件"""
        try:
            if not self._find_element():
                return []

            children = self.element.children()
            logger.debug(f"分组框子控件数量: {len(children)}")
            return children
        except Exception as e:
            logger.error(f"获取分组框子控件失败: {e}")
            return []


class ScrollBarControl(BaseControl):
    """
    滚动条控件 - 封装ScrollBar特有操作
    适用于：ScrollBar
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def set_position(self, pos: int, timeout: int = 10) -> bool:
        """设置滚动条位置"""
        try:
            if not self.wait_enabled(timeout):
                return False

            self.element.set_position(pos)
            logger.info(f"设置滚动条位置: {pos}")
            return True
        except Exception as e:
            logger.error(f"设置滚动条位置失败: {e}")
            return False

    def get_position(self) -> Optional[int]:
        """获取滚动条当前位置"""
        try:
            if not self._find_element():
                return None

            pos = self.element.get_position()
            logger.debug(f"滚动条当前位置: {pos}")
            return pos
        except Exception as e:
            logger.error(f"获取滚动条位置失败: {e}")
            return None

    def scroll_up(self, steps: int = 1, timeout: int = 10) -> bool:
        """向上滚动"""
        try:
            if not self.wait_enabled(timeout):
                return False

            for _ in range(steps):
                self.element.scroll_up()
                time.sleep(0.1)
            logger.info(f"向上滚动 {steps} 步")
            return True
        except Exception as e:
            logger.error(f"向上滚动失败: {e}")
            return False

    def scroll_down(self, steps: int = 1, timeout: int = 10) -> bool:
        """向下滚动"""
        try:
            if not self.wait_enabled(timeout):
                return False

            for _ in range(steps):
                self.element.scroll_down()
                time.sleep(0.1)
            logger.info(f"向下滚动 {steps} 步")
            return True
        except Exception as e:
            logger.error(f"向下滚动失败: {e}")
            return False


class RichEditControl(BaseControl):
    """
    富文本控件 - 封装RichEdit特有操作
    适用于：RichEdit
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def set_text(self, text: str, clear_first: bool = True, timeout: int = 10) -> bool:
        """设置富文本内容"""
        try:
            if not self.wait_enabled(timeout):
                return False

            if clear_first:
                self.element.set_text("")

            self.element.set_text(text)
            logger.info(f"设置富文本内容成功: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"设置富文本内容失败: {e}")
            return False

    def get_text(self) -> Optional[str]:
        """获取富文本纯文本内容"""
        try:
            if not self._find_element():
                return None

            text = self.element.get_value()
            logger.debug(f"富文本内容: {text[:50]}...")
            return text
        except Exception as e:
            logger.error(f"获取富文本内容失败: {e}")
            return None

    def set_font(self, font_name: str, font_size: int, timeout: int = 10) -> bool:
        """设置选中文本的字体"""
        try:
            if not self.wait_enabled(timeout):
                return False

            self.element.set_font(font_name, font_size)
            logger.info(f"设置富文本字体: {font_name} ({font_size}号)")
            return True
        except Exception as e:
            logger.error(f"设置富文本字体失败: {e}")
            return False


class LabelControl(BaseControl):
    """
    标签控件 - 封装Label/Static特有操作
    适用于：Label, Static
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def get_text(self) -> Optional[str]:
        """获取标签文本"""
        try:
            if not self._find_element():
                return None

            text = self.element.window_text()
            logger.debug(f"标签文本: {text}")
            return text
        except Exception as e:
            logger.error(f"获取标签文本失败: {e}")
            return None

    def is_text_matched(self, expected_text: str, case_sensitive: bool = False) -> bool:
        """检查标签文本是否匹配"""
        try:
            actual_text = self.get_text()
            if actual_text is None:
                return False

            if not case_sensitive:
                actual_text = actual_text.lower()
                expected_text = expected_text.lower()

            return actual_text == expected_text
        except Exception as e:
            logger.error(f"检查标签文本匹配失败: {e}")
            return False


class DialogControl(BaseControl):
    """
    对话框控件 - 封装Dialog特有操作
    适用于：Dialog
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def close(self, timeout: int = 10) -> bool:
        """关闭对话框"""
        try:
            if not self.wait_visible(timeout):
                return False

            self.element.close()
            logger.info(f"关闭对话框: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"关闭对话框失败: {e}")
            return False

    def get_dialog_title(self) -> Optional[str]:
        """获取对话框标题"""
        try:
            if not self._find_element():
                return None

            title = self.element.window_text()
            logger.debug(f"对话框标题: {title}")
            return title
        except Exception as e:
            logger.error(f"获取对话框标题失败: {e}")
            return None

    def confirm(self, confirm_button: str = "确定", timeout: int = 10) -> bool:
        """点击确认按钮"""
        try:
            btn = ButtonControl(self.element, title=confirm_button)
            return btn.click(timeout=timeout)
        except Exception as e:
            logger.error(f"确认对话框失败: {e}")
            return False

    def cancel(self, cancel_button: str = "取消", timeout: int = 10) -> bool:
        """点击取消按钮"""
        try:
            btn = ButtonControl(self.element, title=cancel_button)
            return btn.click(timeout=timeout)
        except Exception as e:
            logger.error(f"取消对话框失败: {e}")
            return False


class ImageControl(BaseControl):
    """
    图片控件 - 封装Image特有操作
    适用于：Image
    """

    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)

    def click_input(self, timeout: int = 10) -> bool:
        """
        模拟真实鼠标点击图片控件

        Args:
            timeout: 等待控件可用的超时时间

        Returns:
            bool: 是否成功点击
        """
        try:
            if not self.wait_enabled(timeout):
                logger.error(f"图片控件不可点击: {self.locator}")
                return False

            self.set_focus()
            self.element.click_input()
            logger.info(f"点击图片控件成功: {self.locator}")
            return True
        except Exception as e:
            logger.error(f"点击图片控件失败: {self.locator}, 错误: {e}")
            return False

    def capture_as_image(self, file_path: Optional[str] = None):
        """
        截图图片控件

        Args:
            file_path: 保存路径（可选）

        Returns:
            PIL.Image 对象或 None
        """
        return super().capture_as_image(file_path)

    def get_image_size(self) -> Optional[tuple]:
        """
        获取图片控件的尺寸

        Returns:
            (width, height) 或 None
        """
        rect = self.get_rectangle()
        if rect:
            return (rect[2] - rect[0], rect[3] - rect[1])
        return None
