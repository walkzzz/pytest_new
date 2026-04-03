import logging
import time
from typing import List, Optional, Union

import psutil
from pywinauto.application import WindowSpecification
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError

from pywinauto import Application

logger = logging.getLogger(__name__)


class ApplicationManager:
    """
    应用管理类 - 封装应用的启动、连接、关闭、等待等核心操作

    核心能力：
    1. 启动新应用 / 附加到已有应用（按进程名/句柄/PID）
    2. 安全关闭应用（窗口关闭 / 强制结束进程）
    3. 等待窗口加载、等待进程退出
    4. 检查应用运行状态、获取窗口对象
    """

    def __init__(self):
        self.app: Optional[Application] = None
        self.process: Optional[psutil.Process] = None
        self.start_args: Optional[dict] = None
        self.attached: bool = False

    def _get_process_by_criteria(
        self, process_name: Optional[str] = None, pid: Optional[int] = None, handle: Optional[int] = None
    ) -> Optional[psutil.Process]:
        """
        内部方法：根据进程名/PID/句柄查找进程
        """
        try:
            if pid:
                return psutil.Process(pid)

            if handle:
                from pywinauto import win32functions

                pid = win32functions.GetWindowThreadProcessId(handle)[1]
                return psutil.Process(pid)

            if process_name:
                for proc in psutil.process_iter(["name", "pid"]):
                    if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
                        return proc

            return None
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
            logger.error(f"查找进程失败: {str(e)}")
            return None

    def start(
        self, app_path: str, timeout: int = 30, retry_interval: float = 0.5, backend: str = "win32", **kwargs
    ) -> bool:
        """
        启动新应用

        Args:
            app_path: 应用可执行文件路径
            timeout: 启动超时时间（秒）
            retry_interval: 状态检查重试间隔（秒）
            backend: 使用的后端 (win32/uia)
            **kwargs: 传递给pywinauto.Application.start的额外参数

        Returns:
            bool: 是否启动成功
        """
        try:
            import subprocess

            self.start_args = {"app_path": app_path, "timeout": timeout, "kwargs": kwargs}

            logger.info(f"启动应用: {app_path} | 后端: {backend} | 参数: {kwargs}")

            proc = subprocess.Popen(app_path, **kwargs)
            self.app = Application(backend=backend).connect(process=proc.pid)

            start_time = time.time()
            while time.time() - start_time < timeout:
                self.process = self._get_process_by_criteria(pid=proc.pid)
                if self.process and self.process.is_running():
                    self.attached = False
                    logger.info(f"应用启动成功 | PID: {self.process.pid} | 进程名: {self.process.name()}")
                    return True
                time.sleep(retry_interval)

            logger.error(f"应用启动超时（{timeout}秒）: {app_path}")
            return False

        except Exception as e:
            logger.error(f"应用启动失败: {app_path} | 错误: {str(e)}")
            self.app = None
            self.process = None
            return False

    def attach(
        self,
        process_name: Optional[str] = None,
        pid: Optional[int] = None,
        handle: Optional[int] = None,
        backend: str = "uia",
    ) -> bool:
        """
        附加到已运行的应用

        Args:
            process_name: 进程名
            pid: 进程ID
            handle: 窗口句柄
            backend: pywinauto后端

        Returns:
            bool: 是否附加成功
        """
        try:
            self.process = self._get_process_by_criteria(process_name, pid, handle)
            if not self.process:
                logger.error(f"未找到目标进程 | 进程名: {process_name} | PID: {pid} | 句柄: {handle}")
                return False

            logger.info(f"附加到应用 | PID: {self.process.pid} | 进程名: {self.process.name()}")
            self.app = Application(backend=backend).connect(process=self.process.pid, timeout=10)
            self.attached = True
            logger.info("应用附加成功")
            return True

        except Exception as e:
            logger.error(f"应用附加失败 | 错误: {str(e)}")
            self.app = None
            self.process = None
            return False

    def connect(self, **kwargs) -> bool:
        """
        统一连接方法（自动选择启动/附加）
        """
        if "app_path" in kwargs:
            return self.start(
                app_path=kwargs["app_path"],
                timeout=kwargs.get("timeout", 30),
                retry_interval=kwargs.get("retry_interval", 0.5),
                **{k: v for k, v in kwargs.items() if k not in ["app_path", "timeout", "retry_interval"]},
            )
        else:
            return self.attach(
                process_name=kwargs.get("process_name"),
                pid=kwargs.get("pid"),
                handle=kwargs.get("handle"),
                backend=kwargs.get("backend", "uia"),
            )

    def close(self, window_title: Optional[str] = None, timeout: int = 20, force_kill: bool = True) -> bool:
        """
        关闭应用（优先优雅关闭窗口，失败则强制结束进程）
        """
        if not self.app and not self.process:
            logger.warning("无已连接的应用，无需关闭")
            return True

        try:
            if window_title:
                window = self.app.window(title=window_title)
                if window.exists():
                    logger.info(f"关闭窗口: {window_title}")
                    window.close()
            else:
                logger.info("关闭应用主窗口")
                self.app.kill(soft=True)

            if self.process and self.wait_process_exit(timeout=timeout):
                logger.info("应用优雅关闭成功")
                self._clear()
                return True

        except (ElementNotFoundError, TimeoutError, Exception) as e:
            logger.warning(f"优雅关闭失败: {str(e)}")

        if force_kill and self.process:
            try:
                logger.info(f"强制结束进程 | PID: {self.process.pid}")
                self.process.terminate()
                self.wait_process_exit(timeout=timeout)
                logger.info("进程强制结束成功")
                self._clear()
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
                logger.error(f"强制结束进程失败: {str(e)}")

        self._clear()
        return False

    def kill(self) -> bool:
        """
        强制结束应用进程
        """
        return self.close(force_kill=True, timeout=10)

    def wait_window(
        self, window_title: Union[str, List[str]], timeout: int = 30, retry_interval: float = 0.5, state: str = "exists"
    ) -> Optional[WindowSpecification]:
        """
        等待指定窗口出现并达到指定状态
        """
        if not self.app:
            logger.error("未连接应用，无法等待窗口")
            return None

        titles = [window_title] if isinstance(window_title, str) else window_title
        start_time = time.time()

        while time.time() - start_time < timeout:
            for title in titles:
                try:
                    window = self.app.window(title=title)
                    window.wait(state, timeout=1)
                    logger.info(f"窗口已就绪 | 标题: {title} | 状态: {state}")
                    return window
                except (ElementNotFoundError, TimeoutError):
                    continue
            time.sleep(retry_interval)

        logger.error(f"等待窗口超时（{timeout}秒） | 标题: {titles} | 状态: {state}")
        return None

    def wait_process_exit(self, timeout: int = 20) -> bool:
        """
        等待进程退出
        """
        if not self.process:
            return True

        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.process.is_running():
                return True
            time.sleep(0.5)

        logger.error(f"等待进程退出超时（{timeout}秒） | PID: {self.process.pid}")
        return False

    def get_window(self, **locator) -> Optional[WindowSpecification]:
        """
        获取指定窗口对象
        """
        if not self.app:
            logger.error("未连接应用，无法获取窗口")
            return None

        try:
            window = self.app.window(**locator)
            if window.exists(timeout=1):
                return window
            logger.warning(f"窗口未找到 | 定位参数: {locator}")
            return None
        except Exception as e:
            logger.error(f"获取窗口失败 | 定位参数: {locator} | 错误: {str(e)}")
            return None

    def is_running(self) -> bool:
        """
        检查应用是否正在运行
        """
        if self.process:
            try:
                return self.process.is_running()
            except psutil.NoSuchProcess:
                return False
        return False

    def _clear(self):
        """
        清空应用状态
        """
        self.app = None
        self.process = None
        self.start_args = None
        self.attached = False

    def __del__(self):
        """
        析构函数：确保应用关闭
        """
        if not self.attached and self.is_running():
            logger.info("析构函数触发，自动关闭应用")
            self.close(force_kill=True, timeout=10)
