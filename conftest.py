import os
import time
import pytest
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager
from typing import Optional

SCREENSHOT_DIR = Path(r"D:\TraeWorkspace\tryit\pytest_new")


class ScreenRecorder:
    """屏幕录制和截图工具"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.frames = []
        self._start_time = None
        self._recording = False

    def start_recording(self):
        """开始录制"""
        self._start_time = time.time()
        self._recording = True
        self.frames = []

    def stop_recording(self, test_name: str) -> str:
        """停止录制并生成视频"""
        if not self._recording:
            return ""

        self._recording = False
        if not self.frames:
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in test_name if c.isalnum() or c in ("_", "-"))
        video_path = self.output_dir / f"{safe_name}_{timestamp}.avi"

        try:
            self._create_video(str(video_path))
            return str(video_path)
        except Exception as e:
            print(f"录制视频失败: {e}")
            return ""

    def capture_frame(self, step_name: str = "", action_name: str = ""):
        """捕获帧"""
        if not self._recording:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        step = "".join(c for c in step_name[:20] if c.isalnum() or c == "_")
        action = "".join(c for c in action_name[:20] if c.isalnum() or c == "_")

        filename = f"{step}_{action}_{timestamp}.png"
        filepath = self.output_dir / filename

        try:
            self._capture_screen(str(filepath))
            self.frames.append(filepath)
        except Exception as e:
            print(f"截图失败: {e}")

    def _capture_screen(self, filepath: str):
        """使用mss截屏"""
        try:
            import mss

            with mss.mss() as sct:
                sct.grab(sct.monitors[1]).save(filepath)
        except ImportError:
            self._capture_screen_pil(filepath)

    def _capture_screen_pil(self, filepath: str):
        """使用PIL截屏（备用方案）"""
        try:
            from PIL import ImageGrab

            img = ImageGrab.grab()
            img.save(filepath)
        except Exception as e:
            print(f"PIL截屏失败: {e}")

    def _create_video(self, output_path: str):
        """将帧合成为视频"""
        if not self.frames:
            return

        try:
            import cv2
        except ImportError:
            self._create_gif(output_path.replace(".avi", ".gif"))
            return

        frames = []
        for frame_path in self.frames:
            if os.path.exists(frame_path):
                frame = cv2.imread(str(frame_path))
                if frame is not None:
                    frames.append(frame)

        if not frames:
            return

        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_path, fourcc, 2.0, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()

    def _create_gif(self, output_path: str):
        """将帧合成为GIF（备用方案）"""
        if not self.frames:
            return

        try:
            from PIL import Image

            images = []
            for frame_path in self.frames:
                if os.path.exists(frame_path):
                    img = Image.open(frame_path)
                    images.append(img.copy())

            if images:
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:],
                    duration=500,
                    loop=0,
                )
        except Exception as e:
            print(f"创建GIF失败: {e}")


@pytest.fixture(scope="session")
def screen_recorder():
    """屏幕录制器fixture"""
    return ScreenRecorder(SCREENSHOT_DIR)


@pytest.fixture(autouse=True)
def test_hook(request, screen_recorder):
    """每个测试的钩子 - 自动录屏和截图"""
    test_name = request.node.name
    screen_recorder.start_recording()

    yield

    video_path = screen_recorder.stop_recording(test_name)
    if video_path and os.path.exists(video_path):
        print(f"\n测试视频: {video_path}")
