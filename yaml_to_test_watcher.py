import os
import sys
import time
import warnings

import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def parse_yaml_test_cases(yaml_path):
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        test_cases = data.get("test_cases", {}) if data else {}
        test_data = data.get("test_data", {}) if data else {}
        project_name = (
            data.get(
                "project_name",
                data.get("app", {}).get("project_name", "自动化测试项目"),
            )
            if data
            else "自动化测试项目"
        )
        return test_cases, test_data, project_name
    except Exception as e:
        warnings.warn(f"解析yaml文件失败: {yaml_path}, 错误: {e}")
        return {}, {}, "自动化测试项目"


def generate_test_content(filename, test_cases, test_data, project_name):
    class_name = "".join(word.capitalize() for word in filename.replace(".yaml", "").replace("_", " ").split())

    lines = [
        "import pytest",
        "from src.pytest_runner import BaseTestCase",
        "",
        "",
        f"class Test{class_name}(BaseTestCase):",
        f'    config_filename = "configs/{filename}"',
        f'    project_name = "{project_name}"',
        "",
    ]

    if not test_cases:
        lines.append("    def test_placeholder(self):")
        lines.append('        """Auto-generated test - no test cases found in config"""')
        lines.append("        pass")
        warnings.warn(f"警告: {filename} 中未找到测试用例，已使用占位符")
    else:
        for case_name, case_data in test_cases.items():
            if not test_data:
                lines.append(f"    def test_{case_name}(self):")
                lines.append(f'        """{case_data.get("description", case_name)}"""')
                lines.append(f'        self.run_test_case("{case_name}")')
                lines.append("")
            else:
                for data_key in test_data.keys():
                    test_method_name = f"{case_name}_{data_key}"
                    lines.append(f"    def test_{test_method_name}(self):")
                    lines.append(f'        """{case_data.get("description", case_name)} - {data_key}"""')
                    lines.append(f'        self.run_test_case("{case_name}", data_key="{data_key}")')
                    lines.append("")

    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append('    pytest.main([__file__, "-v", "--tb=short"])')

    return "\n".join(lines)


class YamlToTestHandler(FileSystemEventHandler):
    def __init__(self, config_dir, test_dir):
        self.config_dir = config_dir
        self.test_dir = test_dir
        super().__init__()

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".yaml"):
            yaml_path = event.src_path
            filename = os.path.basename(yaml_path)
            test_name = f"test_{filename.replace('.yaml', '')}.py"
            test_path = os.path.join(self.test_dir, test_name)

            if os.path.exists(test_path):
                print(f"跳过: {test_name} 已存在")
                return

            test_cases, test_data, project_name = parse_yaml_test_cases(yaml_path)
            content = generate_test_content(filename, test_cases, test_data, project_name)

            with open(test_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Created: {test_path}")
            if not test_cases:
                print(f"警告: {filename} 中未找到测试用例，已生成占位符测试方法")


def run_watcher(config_dir, test_dir):
    event_handler = YamlToTestHandler(config_dir, test_dir)
    observer = Observer()
    observer.schedule(event_handler, config_dir, recursive=False)
    observer.start()
    print(f"Watching {config_dir} for new yaml files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    config_dir = r"D:\TraeWorkspace\tryit\pytest_new\tests\configs"
    test_dir = r"D:\TraeWorkspace\tryit\pytest_new\tests"
    run_watcher(config_dir, test_dir)
