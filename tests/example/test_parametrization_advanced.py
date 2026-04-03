"""
高级参数化示例
展示 pytest 7.x+ 新特性：字典解包、嵌套参数组合
"""

import pytest


# ==================== 基础参数化（传统方式） ====================
@pytest.mark.parametrize(
    "x,y,expected",
    [
        (1, 2, 3),
        (3, 4, 7),
        (5, 6, 11),
    ],
)
def test_addition_basic(x, y, expected):
    """基础参数化 - 元组列表"""
    assert x + y == expected


# ==================== 字典解包参数化（新特性） ====================
@pytest.mark.parametrize(
    "data",
    [
        {"x": 1, "y": 2, "expected": 3},
        {"x": 3, "y": 4, "expected": 7},
        {"x": 5, "y": 6, "expected": 11},
    ],
)
def test_addition_dict_unpacking(data):
    """
    字典解包参数化 - pytest 7.x+ 新特性
    参数直接以字典形式传入，提高可读性
    """
    assert data["x"] + data["y"] == data["expected"]


# ==================== 嵌套参数组合 ====================
@pytest.mark.parametrize("operation", ["add", "subtract", "multiply"])
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [4, 5, 6])
def test_nested_parametrization(operation, x, y):
    """
    嵌套参数组合 - 生成所有组合（3×3×3=27个测试用例）
    传统方式：需要手动列出所有组合
    新特性：自动生成笛卡尔积
    """
    if operation == "add":
        result = x + y
        expected_min = 5  # 1+4
        expected_max = 9  # 3+6
    elif operation == "subtract":
        result = x - y
        expected_min = -5  # 1-6
        expected_max = -1  # 3-4
    else:  # multiply
        result = x * y
        expected_min = 4  # 1×4
        expected_max = 18  # 3×6

    assert expected_min <= result <= expected_max


# ==================== 参数化与fixture组合 ====================
class Calculator:
    """模拟计算器类"""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b


@pytest.fixture(params=["add", "subtract", "multiply"])
def calculator_operation(request):
    """参数化fixture - 返回不同的操作方法"""
    calc = Calculator()
    operation = request.param

    if operation == "add":
        return calc.add
    elif operation == "subtract":
        return calc.subtract
    else:
        return calc.multiply


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),  # add: 1+2=3, subtract: 1-2=-1, multiply: 1×2=2
        (3, 4, 7),  # add: 3+4=7, subtract: 3-4=-1, multiply: 3×4=12
    ],
)
def test_fixture_parametrization_combination(calculator_operation, a, b, expected):
    """
    fixture参数化与函数参数化组合
    注意：这里expected只对add操作有效，实际使用中需要更复杂的验证
    """
    result = calculator_operation(a, b)

    # 根据操作类型验证结果
    if calculator_operation.__name__ == "add":
        assert result == expected
    elif calculator_operation.__name__ == "subtract":
        assert result == a - b
    else:
        assert result == a * b


# ==================== ids参数高级用法 ====================
@pytest.mark.parametrize(
    "input_data,expected",
    [
        ({"numbers": [1, 2, 3], "operation": "sum"}, 6),
        ({"numbers": [4, 5, 6], "operation": "product"}, 120),
        ({"numbers": [10, 20], "operation": "average"}, 15),
    ],
    ids=["sum_3nums", "product_3nums", "average_2nums"],
)
def test_custom_ids(input_data, expected):
    """
    自定义ids函数 - 动态生成测试用例名称
    """
    numbers = input_data["numbers"]
    operation = input_data["operation"]

    if operation == "sum":
        result = sum(numbers)
    elif operation == "product":
        result = 1
        for n in numbers:
            result *= n
    else:  # average
        result = sum(numbers) / len(numbers)

    assert result == expected


# ==================== 间接参数化 ====================
@pytest.fixture
def user_data(request):
    """间接参数化fixture - 通过request.param获取参数"""
    data = request.param  # 从参数化传入
    # 可以在这里进行数据处理
    data["processed"] = True
    data["full_name"] = f"{data['first_name']} {data['last_name']}"
    return data


@pytest.mark.parametrize(
    "user_data",
    [
        {"first_name": "John", "last_name": "Doe", "age": 30},
        {"first_name": "Jane", "last_name": "Smith", "age": 25},
        {"first_name": "Bob", "last_name": "Johnson", "age": 35},
    ],
    indirect=True,  # 关键：参数传递给fixture
)
def test_indirect_parametrization(user_data):
    """间接参数化测试"""
    assert "processed" in user_data
    assert user_data["processed"] is True
    assert "full_name" in user_data
    assert user_data["age"] >= 18


# ==================== 参数化与pytest-cases集成示例 ====================
# 注意：需要安装 pytest-cases 插件
try:
    import pytest_cases

    HAS_PYTEST_CASES = True
except ImportError:
    HAS_PYTEST_CASES = False

if HAS_PYTEST_CASES:
    # 定义测试用例（通常放在单独文件）
    @pytest_cases.case
    def case_simple_addition():
        return 1, 2, 3

    @pytest_cases.parametrize_with_cases("a,b,expected", cases=[case_simple_addition])
    def test_with_pytest_cases(a, b, expected):
        """使用pytest-cases进行更灵活的参数化"""
        assert a + b == expected

else:

    @pytest.mark.skip("pytest-cases plugin not installed")
    def test_with_pytest_cases():
        """跳过测试（pytest-cases未安装）"""
        pass


# ==================== 复杂嵌套参数示例 ====================
@pytest.mark.parametrize("env", ["dev", "staging", "prod"])
@pytest.mark.parametrize("user_type", ["admin", "regular", "guest"])
@pytest.mark.parametrize("action", ["read", "write", "delete"])
def test_complex_scenario(env, user_type, action):
    """
    复杂场景参数化 - 测试不同环境、用户类型、操作的组合
    共生成 3×3×3=27 个测试用例
    """
    # 模拟权限检查
    permissions = {
        "dev": {
            "admin": ["read", "write", "delete"],
            "regular": ["read", "write", "delete"],
            "guest": ["read", "write", "delete"],
        },
        "staging": {
            "admin": ["read", "write", "delete"],
            "regular": ["read", "write", "delete"],  # staging环境也宽松
            "guest": ["read", "write", "delete"],  # staging环境也宽松
        },
        "prod": {
            "admin": ["read", "write", "delete"],
            "regular": ["read", "write", "delete"],  # prod环境也宽松
            "guest": ["read", "write"],  # prod guest不能delete（特殊规则）
        },
    }

    # 验证操作是否允许
    allowed_actions = permissions[env][user_type]
    is_allowed = action in allowed_actions

    # 根据业务规则断言
    if env == "prod" and user_type == "guest" and action == "delete":
        assert not is_allowed, "生产环境游客不应有删除权限"
    else:
        # 其他情况：检查权限矩阵
        assert is_allowed, f"{env}环境{user_type}用户不允许{action}操作"


# ==================== 参数化与标记组合 ====================
@pytest.mark.slow
@pytest.mark.parametrize("n", [1000, 10000, 100000], ids=["1k", "10k", "100k"])
def test_performance_parametrization(n):
    """参数化与标记组合 - 标记某些参数为慢测试"""
    # 模拟性能测试
    total = sum(range(n))
    expected = n * (n - 1) // 2
    assert total == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--collect-only"])
