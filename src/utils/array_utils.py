# src/utils/array_utils.py
from typing import List, Dict, Any


def filter_object_array(
    array: List[Dict[str, Any]], key: str, prefix: str
) -> List[Dict[str, Any]]:
    """
    Filter an array of objects based on a key's value starting with a prefix.
    """
    return [obj for obj in array if obj.get(key, "").startswith(prefix)]
