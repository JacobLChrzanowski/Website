#!python3
from typing import Any

def new_dict_exclude_key(entire_dict: dict[Any, Any], remove_key: Any) -> dict[Any, Any]:
    """
    Create a new dictionary by excluding a specified key and its associated value.

    Parameters:
    - original_dict (dict): The input dictionary.
    - key_to_exclude (str): The key to be excluded from the dictionary.

    Returns:
    - dict: A new dictionary without the specified key and its associated value.

    Example:
    >>> input_dict = {'a': 1, 'b': 2, 'c': 3}
    >>> new_dict = exclude_key(input_dict, 'b')
    {'a': 1, 'c': 3}
    """
    copied_dict = entire_dict.copy()
    del copied_dict[remove_key]
    return copied_dict