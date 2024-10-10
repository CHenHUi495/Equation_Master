pip install pytest
# math_operations.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b
# test_math_operations.py

import pytest
from math_operations import add, subtract, multiply, divide

# 测试加法
def test_add():
    assert add(3, 2) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

# 测试减法
def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(0, 0) == 0
    assert subtract(-1, 1) == -2

# 测试乘法
def test_multiply():
    assert multiply(3, 3) == 9
    assert multiply(-1, 1) == -1
    assert multiply(0, 100) == 0

# 测试除法
def test_divide():
    assert divide(10, 2) == 5
    assert divide(3, 1) == 3
    with pytest.raises(ValueError):  # 检查是否抛出异常
        divide(10, 0)
pytest
pytest -v
