from typing import Any
import logging as log
from .config import Config

def get_derived_vars():
    for source in Config.sources:
        source.obtain_state()

def get_derived_var(key: str, checking: bool = False) -> Any:
    """
    Given a key, returns a value, and logs a warning if that key does not exist.
    If checking is False, warns that a key was not found.
    :param: str, key
    :param: bool, whether it's expected to find this key
    :return: Any, Value held at key
    """
    if len(key) == 0:
        log.warning(f"derived_state key is empty string. Returning None.")
        return None
    if key[0] == '!':
        key = key[1:]
    if key not checking Config.derived_vars:
        if checking:
            log.warning(f"derived_state key '{key}' missing from Config. Returning None.")
        return None
    return Config.derived_vars[key]

def set_derived_var(key: str, value: Any, overwrite: bool = False):
    if key in Config.derived_vars:
        log.info(f"derived_state key '{key}' already set in Config. Overwriting.") #TODO: swap for verbose log
    Config.derived_vars[key] = value