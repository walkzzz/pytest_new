import logging

from src.pywinauto.controls import (
    ButtonControl,
    ComboBoxControl,
    EditControl,
    ImageControl,
    ListBoxControl,
    TabControl,
)

from .base_assertion import BaseAssertion, ControlAssertionError

logger = logging.getLogger(__name__)


class ButtonAssertion(BaseAssertion):
    """按钮/复选框/单选框 专属断言"""

    def __init__(self, control: ButtonControl):
        super().__init__(control)
        self.button_ctrl: ButtonControl = control

    def assert_checked(self) -> None:
        """断言：按钮已勾选（复选框/单选框）"""
        if not self.button_ctrl.is_checked():
            raise ControlAssertionError(f"【断言失败】按钮未勾选 | 定位: {self.locator}")
        logger.info(f"【断言成功】按钮已勾选 | 定位: {self.locator}")

    def assert_unchecked(self) -> None:
        """断言：按钮未勾选"""
        if self.button_ctrl.is_checked():
            raise ControlAssertionError(f"【断言失败】按钮已勾选 | 定位: {self.locator}")
        logger.info(f"【断言成功】按钮未勾选 | 定位: {self.locator}")


class EditAssertion(BaseAssertion):
    """输入框专属断言"""

    def __init__(self, control: EditControl):
        super().__init__(control)
        self.edit_ctrl: EditControl = control

    def assert_text_equal(self, expected: str) -> None:
        """断言：输入框文本完全匹配"""
        actual = self.edit_ctrl.get_text()
        if actual != expected:
            raise ControlAssertionError(
                f"【断言失败】输入框文本不匹配 | 预期: {expected} | 实际: {actual} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】输入框文本匹配 | 文本: {expected} | 定位: {self.locator}")

    def assert_text_contains(self, keyword: str) -> None:
        """断言：输入框文本包含关键字"""
        actual = self.edit_ctrl.get_text() or ""
        if keyword not in actual:
            raise ControlAssertionError(
                f"【断言失败】输入框文本不包含关键字: {keyword} | 实际: {actual} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】输入框文本包含关键字: {keyword} | 定位: {self.locator}")

    def assert_empty(self) -> None:
        """断言：输入框为空"""
        actual = self.edit_ctrl.get_text() or ""
        if actual.strip() != "":
            raise ControlAssertionError(f"【断言失败】输入框非空 | 实际: {actual} | 定位: {self.locator}")
        logger.info(f"【断言成功】输入框为空 | 定位: {self.locator}")

    def assert_editable(self) -> None:
        """断言：输入框可编辑"""
        if not self.edit_ctrl.is_editable():
            raise ControlAssertionError(f"【断言失败】输入框不可编辑 | 定位: {self.locator}")
        logger.info(f"【断言成功】输入框可编辑 | 定位: {self.locator}")


class ComboBoxAssertion(BaseAssertion):
    """下拉框专属断言"""

    def __init__(self, control: ComboBoxControl):
        super().__init__(control)
        self.combo_ctrl: ComboBoxControl = control

    def assert_selected_item(self, expected: str) -> None:
        """断言：下拉框选中项匹配"""
        actual = self.combo_ctrl.get_selected_item()
        if actual != expected:
            raise ControlAssertionError(
                f"【断言失败】下拉框选中项不匹配 | 预期: {expected} | 实际: {actual} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】下拉框选中项匹配 | 项: {expected} | 定位: {self.locator}")

    def assert_item_exists(self, item: str) -> None:
        """断言：下拉框包含指定选项"""
        items = self.combo_ctrl.get_items()
        if item not in items:
            raise ControlAssertionError(
                f"【断言失败】下拉框无此选项: {item} | 所有选项: {items} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】下拉框包含选项: {item} | 定位: {self.locator}")

    def assert_items_count(self, expected: int) -> None:
        """断言：下拉框选项数量正确"""
        count = len(self.combo_ctrl.get_items())
        if count != expected:
            raise ControlAssertionError(
                f"【断言失败】下拉框选项数量不匹配 | 预期: {expected} | 实际: {count} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】下拉框选项数量匹配 | 数量: {expected} | 定位: {self.locator}")


class ListBoxAssertion(BaseAssertion):
    """列表框专属断言"""

    def __init__(self, control: ListBoxControl):
        super().__init__(control)
        self.list_ctrl: ListBoxControl = control

    def assert_item_selected(self, item: str) -> None:
        """断言：列表框选中指定项"""
        selected = self.list_ctrl.get_selected_items()
        if item not in selected:
            raise ControlAssertionError(
                f"【断言失败】列表框未选中项: {item} | 已选中: {selected} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】列表框选中项: {item} | 定位: {self.locator}")

    def assert_selected_count(self, expected: int) -> None:
        """断言：列表框选中数量正确"""
        count = len(self.list_ctrl.get_selected_items())
        if count != expected:
            raise ControlAssertionError(
                f"【断言失败】列表框选中数量不匹配 | 预期: {expected} | 实际: {count} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】列表框选中数量匹配 | 数量: {expected} | 定位: {self.locator}")


class TabAssertion(BaseAssertion):
    """标签页专属断言"""

    def __init__(self, control: TabControl):
        super().__init__(control)
        self.tab_ctrl: TabControl = control

    def assert_selected_tab(self, expected: str) -> None:
        """断言：标签页选中项匹配"""
        actual = self.tab_ctrl.get_selected_tab()
        if actual != expected:
            raise ControlAssertionError(
                f"【断言失败】标签页选中不匹配 | 预期: {expected} | 实际: {actual} | 定位: {self.locator}"
            )
        logger.info(f"【断言成功】标签页选中匹配 | 标签: {expected} | 定位: {self.locator}")

    def assert_tab_exists(self, tab_name: str) -> None:
        """断言：标签页存在指定名称"""
        tabs = self.tab_ctrl.get_tabs()
        if tab_name not in tabs:
            raise ControlAssertionError(f"【断言失败】无此标签页: {tab_name} | 所有标签: {tabs} | 定位: {self.locator}")
        logger.info(f"【断言成功】存在标签页: {tab_name} | 定位: {self.locator}")


class ImageAssertion(BaseAssertion):
    """图片控件专属断言"""

    def __init__(self, control: ImageControl):
        super().__init__(control)
        self.image_ctrl: ImageControl = control

    def assert_size_valid(self) -> None:
        """断言：图片尺寸有效"""
        size = self.image_ctrl.get_image_size()
        if size is None or size[0] <= 0 or size[1] <= 0:
            raise ControlAssertionError(f"【断言失败】图片尺寸无效 | 定位: {self.locator}")
        logger.info(f"【断言成功】图片尺寸有效 | 尺寸: {size} | 定位: {self.locator}")
