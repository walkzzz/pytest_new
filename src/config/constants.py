import os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "test_config_template.yaml")

SUPPORTED_CONTROL_TYPES = [
    'base', 'button', 'edit', 'combobox', 'listbox', 'tab', 'tree',
    'progressbar', 'slider', 'calendar', 'statusbar', 'menu', 'toolbar',
    'hyperlink', 'groupbox', 'scrollbar', 'richedit', 'label', 'dialog', 'image'
]

SUPPORTED_EXECUTOR_METHODS = {
    'base': ['wait_visible', 'wait_enabled', 'click', 'double_click', 'right_click',
             'get_property', 'set_focus', 'is_visible', 'is_enabled'],
    'button': ['click', 'is_checked', 'check', 'uncheck'],
    'edit': ['set_text', 'get_text', 'clear_text', 'type_text', 'is_editable'],
    'image': ['click_input', 'capture_as_image', 'get_image_size'],
    'combobox': ['select', 'select_by_index', 'get_items', 'get_selected_item'],
    'listbox': ['select', 'select_by_index', 'get_items', 'get_selected_items'],
    'tab': ['select_tab', 'select_tab_by_index', 'get_tabs', 'get_selected_tab'],
    'tree': ['expand', 'collapse', 'select', 'get_children', 'get_selected_item'],
    'menu': ['click_menu_item', 'get_menu_items', 'is_menu_item_enabled'],
    'toolbar': ['click_button', 'click_button_by_index', 'get_buttons'],
    'dialog': ['close', 'get_dialog_title', 'confirm', 'cancel'],
    'progressbar': ['get_value', 'get_range', 'is_complete'],
    'slider': ['set_value', 'get_value', 'get_range'],
    'calendar': ['set_date', 'get_date', 'set_time', 'get_time'],
    'statusbar': ['get_panel_text', 'get_panel_count'],
    'hyperlink': ['get_link_text', 'get_link_url'],
    'groupbox': ['get_group_text', 'get_children_controls'],
    'scrollbar': ['set_position', 'get_position', 'scroll_up', 'scroll_down'],
    'richedit': ['set_text', 'get_text', 'set_font'],
    'label': ['get_text', 'is_text_matched'],
}

SUPPORTED_ASSERTION_METHODS = {
    'base': ['exists', 'not_exists', 'visible', 'enabled', 'disabled', 'property_equal', 'rect_valid'],
    'button': ['exists', 'not_exists', 'visible', 'enabled', 'disabled', 'property_equal', 'rect_valid',
               'checked', 'unchecked'],
    'edit': ['exists', 'not_exists', 'visible', 'enabled', 'disabled', 'property_equal', 'rect_valid',
             'text_equal', 'text_contains', 'empty', 'editable'],
    'combobox': ['exists', 'not_exists', 'visible', 'enabled', 'disabled', 'property_equal', 'rect_valid',
                 'selected_item', 'item_exists', 'items_count'],
    'listbox': ['exists', 'not_exists', 'visible', 'enabled', 'disabled', 'property_equal', 'rect_valid',
                'item_selected', 'selected_count'],
    'tab': ['exists', 'not_exists', 'visible', 'enabled', 'disabled', 'property_equal', 'rect_valid',
            'selected_tab', 'tab_exists'],
    'image': ['exists', 'not_exists', 'visible', 'enabled', 'disabled', 'property_equal', 'rect_valid', 'size_valid'],
}
