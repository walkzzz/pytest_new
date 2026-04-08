"""
断言辅助工具，提供增强的断言函数和自定义失败信息。

这些函数旨在提供更清晰的测试失败信息，便于快速定位问题。
"""

import difflib
import json
import pprint
from typing import Any, Dict, List, Optional


def assert_equal(
    actual: Any,
    expected: Any,
    message: str = "",
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """
    增强的相等断言，提供详细的差异信息。

    Args:
        actual: 实际值
        expected: 期望值
        message: 自定义错误消息前缀
        context: 额外的上下文信息（如输入参数）

    Raises:
        AssertionError: 当实际值不等于期望值时
    """
    if actual == expected:
        return

    # 构建详细错误信息
    parts = []
    if message:
        parts.append(message)

    parts.append(f"期望: {_format_value(expected)}")
    parts.append(f"实际: {_format_value(actual)}")

    if context:
        parts.append("上下文:")
        for key, value in context.items():
            parts.append(f"  {key}: {_format_value(value)}")

    # 对于字符串，显示差异
    if isinstance(actual, str) and isinstance(expected, str):
        diff = list(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile="期望",
                tofile="实际",
                lineterm="",
            )
        )
        if diff:
            parts.append("差异:")
            parts.extend(diff)

    raise AssertionError("\n".join(parts))


def assert_dict_contains(
    actual: Dict[str, Any],
    expected_subset: Dict[str, Any],
    message: str = "",
) -> None:
    """
    断言字典包含指定的子集。

    Args:
        actual: 实际字典
        expected_subset: 期望的子集
        message: 自定义错误消息
    """
    missing_keys = set(expected_subset.keys()) - set(actual.keys())
    if missing_keys:
        raise AssertionError(f"{message}字典缺少键: {sorted(missing_keys)}\n" f"实际字典: {_format_value(actual)}")

    mismatched = {}
    for key, expected_value in expected_subset.items():
        actual_value = actual[key]
        if actual_value != expected_value:
            mismatched[key] = {
                "期望": expected_value,
                "实际": actual_value,
            }

    if mismatched:
        raise AssertionError(
            f"{message}字典值不匹配:\n" f"{_format_value(mismatched)}\n" f"完整字典: {_format_value(actual)}"
        )


def assert_list_equal(
    actual: List[Any],
    expected: List[Any],
    message: str = "",
    ignore_order: bool = False,
) -> None:
    """
    断言列表相等，可选忽略顺序。

    Args:
        actual: 实际列表
        expected: 期望列表
        message: 自定义错误消息
        ignore_order: 是否忽略顺序（比较集合）
    """
    if ignore_order:
        actual_set = set(actual)
        expected_set = set(expected)
        if actual_set == expected_set:
            return

        extra = actual_set - expected_set
        missing = expected_set - actual_set

        error_msg = f"{message}列表内容不匹配（忽略顺序）"
        if extra:
            error_msg += f"\n多余元素: {_format_value(sorted(extra))}"
        if missing:
            error_msg += f"\n缺少元素: {_format_value(sorted(missing))}"
        raise AssertionError(error_msg)

    if actual == expected:
        return

    # 找出第一个不匹配的位置
    for i, (a, e) in enumerate(zip(actual, expected)):
        if a != e:
            raise AssertionError(
                f"{message}列表在第 {i} 个元素处不匹配:\n"
                f"  期望[{i}]: {_format_value(e)}\n"
                f"  实际[{i}]: {_format_value(a)}\n"
                f"完整期望列表: {_format_value(expected)}\n"
                f"完整实际列表: {_format_value(actual)}"
            )

    if len(actual) != len(expected):
        raise AssertionError(
            f"{message}列表长度不匹配:\n"
            f"  期望长度: {len(expected)}\n"
            f"  实际长度: {len(actual)}\n"
            f"  多余元素: {_format_value(actual[len(expected) :])}\n"
            f"  缺少元素: {_format_value(expected[len(actual) :])}"
        )


def assert_with_context(
    condition: bool,
    message: str = "",
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """
    带上下文的断言，当条件为False时显示上下文信息。

    Args:
        condition: 断言条件
        message: 自定义错误消息
        context: 额外的上下文信息
    """
    if condition:
        return

    parts = [message] if message else ["断言失败"]
    if context:
        parts.append("上下文:")
        for key, value in context.items():
            parts.append(f"  {key}: {_format_value(value)}")

    raise AssertionError("\n".join(parts))


def _format_value(value: Any, max_length: int = 200) -> str:
    """
    格式化值用于错误消息，限制长度。

    Args:
        value: 要格式化的值
        max_length: 最大字符串长度

    Returns:
        格式化后的字符串
    """
    if isinstance(value, (dict, list, tuple, set)):
        try:
            formatted = json.dumps(value, ensure_ascii=False, indent=2)
        except (TypeError, ValueError):
            formatted = pprint.pformat(value, width=80, depth=3)

        if len(formatted) > max_length:
            formatted = formatted[:max_length] + "..."
        return formatted

    str_value = str(value)
    if len(str_value) > max_length:
        return str_value[:max_length] + "..."
    return str_value


# 导出常用断言别名
assert_eq = assert_equal
assert_dict_has = assert_dict_contains
assert_list_eq = assert_list_equal
