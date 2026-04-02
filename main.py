from pywinauto.application import Application


app_path = "D:\\Program Files\\CBIM\\modulelogin.exe"
app = Application(backend="uia").start(app_path)


# app = Application(backend="uia").connect(title="modulelogin")
login_dlg = app.window(title="modulelogin")
# login_dlg.wait('visible', timeout=10)
# login_dlg.print_control_identifiers()

# 点击在线注册按钮
register_btn = login_dlg.child_window(title="在线注册", control_type="Button")
register_btn.click()


# 点击头像
login_avatar = login_dlg.child_window(best_match="Image2")
login_avatar.click_input()
# 输入文件名
filename_edit = login_dlg.child_window(title="文件名(N):", control_type="Edit")
login_dlg.print_control_identifiers()
filename_edit.set_text("avatar_海葵_128x128.png")

# 点击打开按钮
open_btn = login_dlg.child_window(title="打开(O)", control_type="Button")
open_btn.click()

# 点击确认按钮
register_btn = login_dlg.child_window(title="确认", control_type="Button")
register_btn.click()

# login_dlg.print_control_identifiers()
# 选择昵称 ['Edit3']
nickname_edit = login_dlg.child_window(best_match="Edit3")
nickname_edit.set_text("test")

# 选择性别
gender_radio = login_dlg.child_window(title="女", control_type="RadioButton")
gender_radio.click()

# 输入密码
password_edit = login_dlg.child_window(best_match="Edit4")
password_edit.set_text("123456")
# 点击签字图按钮
import_btn = login_dlg.child_window(title="导入签字(图)", control_type="Button")
import_btn.click()

# 输入文件名
filename_edit = login_dlg.child_window(title="文件名(N):", control_type="Edit")
filename_edit.set_text("marker.png")

# # 点击打开按钮
open_btn = login_dlg.child_window(title="打开(O)", control_type="Button")
open_btn.click()

# 点击注册按钮
register_btn = login_dlg.child_window(title="注册", control_type="Button")
register_btn.click()

# 点击是按钮
register_btn = login_dlg.child_window(title="是", control_type="Button")
register_btn.click()