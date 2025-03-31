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

tool_list = [multiply]