import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="自动化测试CLI")
    parser.add_argument("--module", "-m", help="指定测试模块（如login）")
    parser.add_argument("--mark", "-mk", help="指定pytest标签（如smoke）")
    parser.add_argument("--env", "-e", default="test", help="运行环境（dev/test/prod）")
    parser.add_argument("--case", "-c", help="指定测试用例名称")
    parser.add_argument("--parallel", "-n", type=int, default=0, help="并行进程数")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    args = parser.parse_args()

    cmd = [sys.executable, "-m", "pytest"]

    if args.module:
        test_path = Path("tests") / args.module
        if test_path.exists():
            cmd.append(str(test_path))
        else:
            cmd.append(f"tests/{args.module}")
    else:
        cmd.append("tests/")

    if args.mark:
        cmd.extend(["-m", args.mark])

    if args.case:
        cmd.extend(["-k", args.case])

    if args.parallel > 0:
        cmd.extend(["-n", str(args.parallel)])

    if args.verbose:
        cmd.append("-vv")

    cmd.extend(["--alluredir=allure-results", f"--env={args.env}"])

    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
