#!python3
"""
"""
import os
from dotenv import dotenv_values
from .config import Config

def get_dotenv_vars(dotenv_dir: str) -> dict[str, str]:
    dotenv_filepath = os.path.join(dotenv_dir, '.env')
    dotenv_vars = dict(dotenv_values(dotenv_filepath))
    if type(dotenv_vars) != dict:
        dotenv_vars = {}

    if len(dotenv_vars.keys()) == 0:
        raise(Exception("No .env vars?"))

    return dotenv_vars #type: ignore

def get(key: str, exception: Exception) -> str:
    if key not in Config.dotenv_vars:
        raise exception
    else:
        return Config.dotenv_vars[key]