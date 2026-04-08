#!/usr/bin/env python3
"""
测试命名规范检查脚本。

检查测试函数和类是否遵循命名规范：
- 测试函数：test_业务场景_条件_预期结果
- 测试类：Test业务场景

使用方式：
    python scripts/check_test_naming.py [目录]  # 默认为当前目录
"""

import ast
import sys
from pathlib import Path
import re


def check_test_naming(file_path: Path) -> list[str]:
    """检查单个文件的测试命名规范"""
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return [f"文件无法解码: {file_path}"]

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [f"语法错误: {file_path}:{e.lineno}: {e.msg}"]

    for node in ast.walk(tree):
        # 检查测试函数
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            if func_name.startswith("test_"):
                # 检查命名模式：test_业务场景_条件_预期结果
                # 至少要有两个下划线分隔（三个部分）
                parts = func_name.split("_")
                if len(parts) < 3:
                    issues.append(
                        f"{file_path}:{node.lineno}: 测试函数 '{func_name}' "
                        f"应遵循 'test_业务场景_条件_预期结果' 格式（至少包含两个下划线）"
                    )
                # 可选：检查是否包含中文（允许但不强制）
                # if any('\u4e00' <= char <= '\u9fff' for char in func_name):
                #     issues.append(f"{file_path}:{node.lineno}: 测试函数名包含中文: '{func_name}'")

        # 检查测试类
        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            if class_name.startswith("Test"):
                # 检查类名是否以Test开头，后跟业务场景
                if len(class_name) == 4:  # 只有"Test"
                    issues.append(
                        f"{file_path}:{node.lineno}: 测试类 '{class_name}' "
                        f"应包含业务场景，例如 'TestUserLogin'"
                    )
                # 检查是否有测试方法
                has_test_method = False
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith(
                        "test_"
                    ):
                        has_test_method = True
                        break
                if not has_test_method:
                    issues.append(
                        f"{file_path}:{node.lineno}: 测试类 '{class_name}' "
                        f"没有以'test_'开头的测试方法"
                    )

    return issues


def main() -> None:
    """主函数"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(".")

    if not root_dir.exists():
        print(f"错误: 目录不存在: {root_dir}")
        sys.exit(1)

    # 查找所有测试文件
    test_files = []
    for pattern in ["**/test_*.py", "**/*_test.py"]:
        test_files.extend(root_dir.glob(pattern))

    # 排除虚拟环境等目录
    test_files = [
        f
        for f in test_files
        if "venv" not in str(f) and ".env" not in str(f) and "__pycache__" not in str(f)
    ]

    if not test_files:
        print(f"未找到测试文件: {root_dir}")
        sys.exit(0)

    print(f"检查 {len(test_files)} 个测试文件...")

    all_issues = []
    for test_file in sorted(test_files):
        issues = check_test_naming(test_file)
        all_issues.extend(issues)

    if all_issues:
        print("\n发现以下命名规范问题:")
        for issue in all_issues:
            print(f"  {issue}")
        print(f"\n总计: {len(all_issues)} 个问题")
        sys.exit(1)
    else:
        print("所有测试文件命名规范检查通过!")
        sys.exit(0)


if __name__ == "__main__":
    main()
