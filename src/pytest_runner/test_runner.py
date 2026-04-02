import logging
import os
import json
from datetime import datetime
from typing import Any, Dict, Optional

import allure
from allure_commons.types import AttachmentType

SCREENSHOT_DIR = r"D:\TraeWorkspace\tryit\pytest_new\screenshots"

from src.pywinauto.app_manager import ApplicationManager
from src.pywinauto.controls import ControlFactory
from src.pywinauto.action_executors import ActionExecutorFactory
from src.pywinauto.assertions import AssertionFactory, ControlAssertionError
from src.config import Config


class TestRunner:
    """
    测试运行器 - 通用测试执行引擎
    支持配置文件驱动、Allure报告生成
    """

    def __init__(
        self,
        config_path: str,
        app_config: Optional[Dict[str, Any]] = None,
        controls_config: Optional[Dict[str, Any]] = None,
        timeouts: Optional[Dict[str, float]] = None,
        base_url: Optional[str] = None,
        project_name: Optional[str] = None,
        build_name: Optional[str] = None,
        testplan_url: Optional[str] = None,
    ):
        self.config = Config.load_config(config_path)

        errors = Config.validate_config(self.config)
        if errors:
            raise ValueError(f"配置验证失败: {errors}")

        self.app_config = app_config or Config.get_app_config(self.config)
        self.controls_config = controls_config or Config.get_controls_config(
            self.config
        )
        self.timeouts = timeouts or Config.get_timeouts(self.config)

        self.base_url = base_url
        self.project_name = project_name
        self.build_name = build_name
        self.testplan_url = testplan_url

        self.app_mgr = ApplicationManager()
        self.control_factory: Optional[ControlFactory] = None
        self.action_factory: Optional[ActionExecutorFactory] = None
        self.assert_factory = AssertionFactory()
        self.logger = logging.getLogger(__name__)

        self._is_connected = False

    def connect_app(self, auto_start: bool = True) -> bool:
        """连接应用

        Args:
            auto_start: 是否自动启动应用（如果连接失败且配置了app_path）
        """
        if not self._is_connected:
            self.app_config = Config.get_app_config(self.config)
            self.controls_config = Config.get_controls_config(self.config)
            self.timeouts = Config.get_timeouts(self.config)

        if self.app_mgr.connect(
            process_name=self.app_config["process_name"],
            backend=self.app_config["backend"],
        ):
            window = self.app_mgr.wait_window(
                window_title=self.app_config["main_window"]["title"],
                state=self.app_config["main_window"]["state"],
            )
            if window:
                self.control_factory = ControlFactory(window)
                self.action_factory = ActionExecutorFactory(self.control_factory)
                self._is_connected = True
                return True

        if auto_start and "app_path" in self.app_config:
            self.logger.info(f"连接失败，尝试启动应用: {self.app_config['app_path']}")
            self.app_mgr.start(
                app_path=self.app_config["app_path"],
                timeout=self.app_config.get("start_timeout", 30),
                backend=self.app_config.get("backend", "win32"),
            )

            if self.app_mgr.connect(
                process_name=self.app_config["process_name"],
                backend=self.app_config["backend"],
            ):
                window = self.app_mgr.wait_window(
                    window_title=self.app_config["main_window"]["title"],
                    state=self.app_config["main_window"]["state"],
                )
                if window:
                    self.control_factory = ControlFactory(window)
                    self.action_factory = ActionExecutorFactory(self.control_factory)
                    self._is_connected = True
                    return True

        return False

    def disconnect_app(self, close_app: bool = False):
        """断开应用连接

        Args:
            close_app: 是否关闭应用（默认不断开，只断开连接）
        """
        if self._is_connected:
            if close_app:
                self.app_mgr.close()
            self._is_connected = False

    def get_control(self, control_name: str):
        """根据配置获取控件"""
        control_type, locator = Config.get_control_locator(
            self.controls_config, control_name
        )
        return self._create_control(control_type, locator)

    def _create_control(self, control_type: str, locator: dict):
        """根据类型创建控件"""
        factory_map = {
            "button": self.control_factory.button,
            "edit": self.control_factory.edit,
            "image": self.control_factory.image,
            "combobox": self.control_factory.combobox,
            "listbox": self.control_factory.listbox,
            "tab": self.control_factory.tab,
            "tree": self.control_factory.tree,
            "menu": self.control_factory.menu,
            "dialog": self.control_factory.dialog,
            "progressbar": self.control_factory.progressbar,
            "slider": self.control_factory.slider,
            "calendar": self.control_factory.calendar,
            "statusbar": self.control_factory.statusbar,
            "toolbar": self.control_factory.toolbar,
            "hyperlink": self.control_factory.hyperlink,
            "groupbox": self.control_factory.groupbox,
            "scrollbar": self.control_factory.scrollbar,
            "richedit": self.control_factory.richedit,
            "label": self.control_factory.label,
        }

        factory = factory_map.get(control_type, self.control_factory.base)
        return factory(**locator)

    def get_action(self, control_name: str):
        """根据配置获取执行器"""
        control_type, locator = Config.get_control_locator(
            self.controls_config, control_name
        )
        return self._create_action(control_type, locator)

    def _create_action(self, control_type: str, locator: dict):
        """根据类型创建执行器"""
        supported_types = Config.get_supported_executor_methods()

        if control_type in supported_types:
            action_getter = getattr(self.action_factory, control_type, None)
            if action_getter:
                return action_getter(**locator)

        return self.action_factory.base(**locator)

    def execute_action(self, action_config: dict):
        """执行动作"""
        control_name = action_config["control"]
        method = action_config["method"]
        params = action_config.get("params", [])

        action = self.get_action(control_name)
        method_func = getattr(action, method, None)

        if method_func is None:
            raise AttributeError(f"执行器 {control_name} 没有方法 {method}")

        if params:
            method_func(*params)
        else:
            method_func()

    def execute_assertions(self, assertions_config: list):
        """执行断言"""
        for assertion in assertions_config:
            control_name = assertion["control"]
            checks = assertion.get("checks", [])

            control = self.get_control(control_name)
            assertion_obj = self.assert_factory.get_assertion(control)

            for check in checks:
                assert_method = getattr(assertion_obj, f"assert_{check}", None)
                if assert_method:
                    try:
                        assert_method()
                    except ControlAssertionError as e:
                        self.logger.error(f"断言失败: {check} - {e}")
                        raise

    def _capture_screenshot(
        self, step_name: str, action_name: str, control_name: str = None
    ) -> str:
        """截图并保存

        Args:
            step_name: 步骤名称
            action_name: 动作名称
            control_name: 控件名称（可选，截取该控件而非窗口）

        Returns:
            截图文件路径
        """
        if not self._is_connected:
            return ""

        try:
            from PIL import ImageGrab

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_step = "".join(c for c in step_name[:20] if c.isalnum() or c == "_")
            safe_action = "".join(
                c for c in action_name[:20] if c.isalnum() or c == "_"
            )
            filename = f"{safe_step}_{safe_action}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)

            os.makedirs(SCREENSHOT_DIR, exist_ok=True)

            if (
                control_name
                and hasattr(self, "control_factory")
                and self.control_factory
            ):
                try:
                    control = self.get_control(control_name)
                    if control and hasattr(control, "element"):
                        img = control.element.capture_as_image()
                        if img:
                            img.save(filepath)
                        else:
                            raise Exception("控件截图失败")
                    else:
                        raise Exception("控件不存在")
                except Exception:
                    window = self.control_factory.window
                    import time

                    time.sleep(0.3)
                    img = window.capture_as_image()
                    if img:
                        img.save(filepath)
            elif hasattr(self, "control_factory") and self.control_factory:
                window = self.control_factory.window
                import time

                time.sleep(0.3)
                img = window.capture_as_image()
                if img:
                    img.save(filepath)
            else:
                from PIL import ImageGrab

                img = ImageGrab.grab()
                img.save(filepath)

            return filepath if os.path.exists(filepath) else ""
        except Exception as e:
            self.logger.warning(f"截图失败: {e}")
            return ""

    def run_step(self, step: dict, step_index: int = 0, test_data: dict = None):
        """执行单个步骤

        Args:
            step: 步骤配置
            step_index: 步骤索引
            test_data: 测试数据（用于显示在报告中）
        """
        step_name = step.get("name", "未命名步骤")
        action_config = step.get("action", {})
        assertions_config = step.get("assertions", [])
        timeout_key = step.get("timeout", "normal")

        self.logger.info(f"执行步骤: {step_name}")

        step_num = step_index + 1
        control_name = action_config.get("control", "")
        method = action_config.get("method", "")
        params = action_config.get("params", [])

        with allure.step(step_name):
            if test_data:
                allure.attach(
                    str(test_data),
                    "测试数据",
                    AttachmentType.JSON,
                )

            if action_config:
                screenshot_before = self._capture_screenshot(
                    step_name, method, control_name
                )
                if screenshot_before:
                    with open(screenshot_before, "rb") as f:
                        allure.attach(
                            f.read(),
                            f"截图(点击前)",
                            AttachmentType.PNG,
                        )
                    try:
                        os.remove(screenshot_before)
                    except:
                        pass

                self.execute_action(action_config)

                screenshot_after = self._capture_screenshot(
                    step_name, method, control_name
                )
                if screenshot_after:
                    with open(screenshot_after, "rb") as f:
                        allure.attach(
                            f.read(),
                            f"截图(点击后)",
                            AttachmentType.PNG,
                        )
                    try:
                        os.remove(screenshot_after)
                    except:
                        pass

                action_info = f"""{step_name}

**step_action**: {json.dumps(action_config, ensure_ascii=False)}

- 控件: `{control_name}`
- 方法: `{method}`
- 参数: `{params}`
- 超时: `{timeout_key}`"""
                allure.attach(
                    action_info,
                    "动作参数",
                    AttachmentType.TEXT,
                )

            if assertions_config:
                self.execute_assertions(assertions_config)
                allure.attach(
                    str(assertions_config),
                    "断言",
                    AttachmentType.TEXT,
                )

            import time

            timeout = self.timeouts.get(timeout_key, 0.5)
            time.sleep(timeout)

    @allure.suite("测试套件")
    @allure.title("测试套件执行")
    def run_test_case(self, test_case_name: str, data_key: str = None):
        """运行测试用例

        Args:
            test_case_name: 测试用例名称
            data_key: 测试数据 key，用于数据驱动
        """
        # 如果传入 data_key，先获取对应测试数据
        if data_key:
            test_data = self.config.get("test_data", {}).get(data_key, {})
            # 手动解析测试用例，使用传入的 test_data
            test_case = Config.get_test_case(self.config, test_case_name)
            steps = Config.get_test_case_steps(test_case)
            resolved_steps = Config._resolve_steps_template(steps, test_data)
            parsed_case = {
                "name": test_case_name,
                "description": test_case.get("description", ""),
                "test_data": test_data,
                "steps": resolved_steps,
            }
            test_case_config = test_case
        else:
            parsed_case = Config.parse_test_case(self.config, test_case_name)
            test_case_config = Config.get_test_case(self.config, test_case_name)
            test_data = parsed_case.get("test_data", {})

        steps = parsed_case["steps"]

        epic = test_case_config.get("epic", self.project_name or "自动化测试")
        feature = test_case_config.get("feature", "功能测试")
        story = test_case_config.get("story", test_case_name)
        severity = test_case_config.get("severity", "normal")
        tags = test_case_config.get("tags", [])
        suite = test_case_config.get("suite", "默认套件")
        lead = test_case_config.get("lead", "")
        owner = test_case_config.get("owner", "")
        layer = test_case_config.get("layer", "e2e")
        link_url = test_case_config.get("link_url", "")
        link_name = test_case_config.get("link_name", "")
        issue_url = test_case_config.get("issue_url", "")
        issue_name = test_case_config.get("issue_name", "")

        allure.epic(epic)
        allure.feature(feature)
        allure.story(story)
        allure.suite(suite)
        allure.severity(severity)

        if layer:
            allure.tag(layer)
        if tags:
            for tag in tags:
                allure.tag(tag)

        if link_url:
            allure.link(url=link_url, name=link_name or "文档链接")
        if issue_url:
            allure.issue(url=issue_url, name=issue_name or "相关issue")

        if lead:
            allure.label("lead", lead)
        if owner:
            allure.label("owner", owner)

        data_key_display = data_key if data_key else "N/A"

        case_description = test_case_config.get("description", "无描述")

        description_detail = f"""## 测试用例详情

| 字段 | 值 |
|------|-----|
| 用例名称 | `{test_case_name}` |
| 描述 | {case_description} |
| 测试数据key | `{data_key_display}` |
| 昵称 | `{test_data.get("nickname", "N/A")}` |
| 密码 | `{test_data.get("password", "N/A")}` |
| 头像文件 | `{test_data.get("avatar_filename", "N/A")}` |
| 签字文件 | `{test_data.get("signature_filename", "N/A")}` |
| 项目 | {self.project_name or "自动化测试"} |
| 总步骤数 | {len(steps)} |

## 测试数据 (test_data)

```
{json.dumps(test_data, ensure_ascii=False, indent=2)}
```

## 配置信息

- **应用**: {self.app_config.get("process_name", "N/A")}
- **窗口**: {self.app_config.get("main_window", {}).get("title", "N/A")}
- **后端**: {self.app_config.get("backend", "N/A")}"""

        allure.title(f"{test_case_name}: {case_description} - {data_key_display}")
        allure.description(description_detail)

        if self.build_name:
            allure.label("build", self.build_name)
        if self.testplan_url:
            allure.label("testplan", self.testplan_url)

        self.logger.info(f"\n{'=' * 50}")
        self.logger.info(f"开始测试用例: {test_case_name}")
        self.logger.info(f"描述: {parsed_case.get('description', '无描述')}")
        self.logger.info(f"{'=' * 50}")

        for i, step in enumerate(steps):
            try:
                self.run_step(step, i, test_data)
            except ControlAssertionError as e:
                allure.attach(f"步骤 {i + 1} 断言失败", "错误信息", AttachmentType.TEXT)
                raise
            except Exception as e:
                allure.attach(
                    f"步骤 {i + 1} 执行失败: {str(e)}", "错误信息", AttachmentType.TEXT
                )
                raise

        self.logger.info(f"测试用例 '{test_case_name}' 执行完成")

    @allure.suite("测试套件")
    @allure.title("完整测试套件执行")
    def run_all_test_cases(self):
        """运行所有测试用例"""
        test_cases = Config.parse_all_test_cases(self.config)

        self.logger.info("=" * 50)
        self.logger.info("测试套件开始执行")
        self.logger.info(f"共 {len(test_cases)} 个测试用例")
        self.logger.info(f"支持的控制类型: {Config.get_supported_control_types()}")
        self.logger.info("=" * 50)

        for test_case_name in test_cases.keys():
            try:
                self.run_test_case(test_case_name)
            except ControlAssertionError as e:
                self.logger.error(f"断言失败: {e}")
                with allure.step("测试终止: 断言失败"):
                    pass
                break
            except Exception as e:
                self.logger.error(f"执行失败: {e}")
                with allure.step("测试终止: 执行错误"):
                    pass
                break

        self.logger.info("\n" + "=" * 50)
        self.logger.info("测试套件执行完成")
        self.logger.info("=" * 50)

    def __enter__(self):
        """上下文管理器入口"""
        self.connect_app()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect_app()


def run_with_allure(
    config_path: str,
    test_case_name: str = None,
    base_url: str = None,
    project_name: str = None,
    build_name: str = None,
    testplan_url: str = None,
):
    """
    使用Allure报告运行测试

    Args:
        config_path: 配置文件路径
        test_case_name: 测试用例名称（None则运行所有）
        base_url: 基础URL
        project_name: 项目名称
        build_name: 构建名称
        testplan_url: 测试计划URL
    """
    runner = TestRunner(
        config_path=config_path,
        base_url=base_url,
        project_name=project_name,
        build_name=build_name,
        testplan_url=testplan_url,
    )

    if runner.connect_app():
        if test_case_name:
            runner.run_test_case(test_case_name)
        else:
            runner.run_all_test_cases()
        runner.disconnect_app()
    else:
        logging.error("无法连接到应用")
