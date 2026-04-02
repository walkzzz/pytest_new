import logging
import time
from typing import Optional, Tuple, List
from pywinauto.application import WindowSpecification
from .base_control import BaseControl

logger = logging.getLogger(__name__)


class TreeControl(BaseControl):
    """
    树形控件 - 封装TreeView特有操作
    适用于：TreeView
    """
    
    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)
    
    def expand(self, item: str, timeout: int = 10) -> bool:
        """展开指定节点"""
        try:
            if not self.wait_enabled(timeout):
                return False
            
            self.element.expand(item)
            logger.info(f"展开树形节点: '{item}'")
            return True
        except Exception as e:
            logger.error(f"展开树形节点失败: {e}")
            return False
    
    def collapse(self, item: str, timeout: int = 10) -> bool:
        """折叠指定节点"""
        try:
            if not self.wait_enabled(timeout):
                return False
            
            self.element.collapse(item)
            logger.info(f"折叠树形节点: '{item}'")
            return True
        except Exception as e:
            logger.error(f"折叠树形节点失败: {e}")
            return False
    
    def select(self, item: str, timeout: int = 10) -> bool:
        """选择树形节点"""
        try:
            if not self.wait_enabled(timeout):
                return False
            
            self.element.select(item)
            logger.info(f"选择树形节点: '{item}'")
            return True
        except Exception as e:
            logger.error(f"选择树形节点失败: {e}")
            return False
    
    def get_children(self, parent_item: Optional[str] = None) -> list:
        """获取节点子项"""
        try:
            if not self._find_element():
                return []
            
            children = self.element.get_children(parent_item) if parent_item else self.element.get_children()
            logger.debug(f"树形节点子项: {children}")
            return children
        except Exception as e:
            logger.error(f"获取树形节点子项失败: {e}")
            return []
    
    def get_selected_item(self) -> Optional[str]:
        """获取当前选中节点"""
        try:
            if not self._find_element():
                return None
            
            selected = self.element.get_selected_item()
            logger.debug(f"当前选中树形节点: {selected}")
            return selected
        except Exception as e:
            logger.error(f"获取选中树形节点失败: {e}")
            return None


class ProgressBarControl(BaseControl):
    """
    进度条控件 - 封装ProgressBar特有操作
    适用于：ProgressBar
    """
    
    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)
    
    def get_value(self) -> Optional[int]:
        """获取当前进度值"""
        try:
            if not self._find_element():
                return None
            
            value = self.element.get_value()
            logger.debug(f"进度条当前值: {value}")
            return value
        except Exception as e:
            logger.error(f"获取进度条值失败: {e}")
            return None
    
    def get_range(self) -> Optional[Tuple[int, int]]:
        """获取进度条范围 (最小值, 最大值)"""
        try:
            if not self._find_element():
                return None
            
            min_val = self.element.minimum()
            max_val = self.element.maximum()
            logger.debug(f"进度条范围: ({min_val}, {max_val})")
            return (min_val, max_val)
        except Exception as e:
            logger.error(f"获取进度条范围失败: {e}")
            return None
    
    def is_complete(self) -> bool:
        """检查进度条是否完成"""
        try:
            range_vals = self.get_range()
            current = self.get_value()
            if not range_vals or current is None:
                return False
            return current >= range_vals[1]
        except Exception as e:
            logger.error(f"检查进度条完成状态失败: {e}")
            return False


class SliderControl(BaseControl):
    """
    滑块控件 - 封装Slider特有操作
    适用于：Slider, TrackBar
    """
    
    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)
    
    def set_value(self, value: int, timeout: int = 10) -> bool:
        """设置滑块值"""
        try:
            if not self.wait_enabled(timeout):
                return False
            
            self.element.set_value(value)
            logger.info(f"设置滑块值: {value}")
            return True
        except Exception as e:
            logger.error(f"设置滑块值失败: {e}")
            return False
    
    def get_value(self) -> Optional[int]:
        """获取滑块当前值"""
        try:
            if not self._find_element():
                return None
            
            value = self.element.get_value()
            logger.debug(f"滑块当前值: {value}")
            return value
        except Exception as e:
            logger.error(f"获取滑块值失败: {e}")
            return None
    
    def get_range(self) -> Optional[Tuple[int, int]]:
        """获取滑块范围 (最小值, 最大值)"""
        try:
            if not self._find_element():
                return None
            
            min_val = self.element.minimum()
            max_val = self.element.maximum()
            logger.debug(f"滑块范围: ({min_val}, {max_val})")
            return (min_val, max_val)
        except Exception as e:
            logger.error(f"获取滑块范围失败: {e}")
            return None


class CalendarControl(BaseControl):
    """
    日历控件 - 封装Calendar/DateTimePicker特有操作
    适用于：Calendar, DateTimePicker
    """
    
    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)
    
    def set_date(self, date: str, timeout: int = 10) -> bool:
        """设置日期（格式：YYYY-MM-DD）"""
        try:
            if not self.wait_enabled(timeout):
                return False
            
            self.element.set_date(date)
            logger.info(f"设置日历日期: {date}")
            return True
        except Exception as e:
            logger.error(f"设置日历日期失败: {e}")
            return False
    
    def get_date(self) -> Optional[str]:
        """获取当前选中日期"""
        try:
            if not self._find_element():
                return None
            
            date = self.element.get_date()
            logger.debug(f"当前日历日期: {date}")
            return date
        except Exception as e:
            logger.error(f"获取日历日期失败: {e}")
            return None
    
    def set_time(self, time_str: str, timeout: int = 10) -> bool:
        """设置时间（格式：HH:MM:SS）"""
        try:
            if not self.wait_enabled(timeout):
                return False
            
            self.element.set_time(time_str)
            logger.info(f"设置日历时间: {time_str}")
            return True
        except Exception as e:
            logger.error(f"设置日历时间失败: {e}")
            return False
    
    def get_time(self) -> Optional[str]:
        """获取当前选中时间"""
        try:
            if not self._find_element():
                return None
            
            time_val = self.element.get_time()
            logger.debug(f"当前日历时间: {time_val}")
            return time_val
        except Exception as e:
            logger.error(f"获取日历时间失败: {e}")
            return None


class StatusBarControl(BaseControl):
    """
    状态栏控件 - 封装StatusBar特有操作
    适用于：StatusBar
    """
    
    def __init__(self, window: WindowSpecification, **locator):
        super().__init__(window, **locator)
    
    def get_panel_text(self, panel_index: int = 0) -> Optional[str]:
        """获取指定面板文本"""
        try:
            if not self._find_element():
                return None
            
            text = self.element.get_panel_text(panel_index)
            logger.debug(f"状态栏面板 {panel_index} 文本: {text}")
            return text
        except Exception as e:
            logger.error(f"获取状态栏面板文本失败: {e}")
            return None
    
    def get_panel_count(self) -> Optional[int]:
        """获取面板数量"""
        try:
            if not self._find_element():
                return None
            
            count = self.element.panel_count()
            logger.debug(f"状态栏面板数量: {count}")
            return count
        except Exception as e:
            logger.error(f"获取状态栏面板数量失败: {e}")
            return None
