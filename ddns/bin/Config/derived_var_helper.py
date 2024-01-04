from typing import Any
import logging as log
from .config import Config

def get_derived_vars():
    for source in Config.sources:
        source.obtain_state()

def get_derived_var(key: str) -> Any:
    if key not in Config.derived_vars:
        log.info(f"derived_state key '{key}' missing from Config. Returning None.") #TODO: swap for verbose og
        return None
    return Config.derived_vars[key]

def set_derived_var(key: str, value: Any, overwrite: bool = False):
    if key in Config.derived_vars:
        log.info(f"derived_state key '{key}' already set in Config. Overwriting.") #TODO: swap for verbose log
    Config.derived_vars[key] = value