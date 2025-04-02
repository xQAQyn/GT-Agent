from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of the two numbers.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

@tool
def power(a: int, b: int) -> int:
    """Raise a number to the power of another.

    Args:
        a (int): The base number.
        b (int): The exponent.

    Returns:
        int: The result of a raised to the power of b.
    """
    return a ** b

tool_list = [multiply, add, power]