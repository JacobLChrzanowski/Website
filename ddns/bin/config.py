#!/usr/bin/python3
"""
Only used to share config across application. Should only be declared once, and never re-declared.
"""
# from dotmap import DotMap #type: ignore
# https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Registrars.Default import Default_Registrar

class Config_Obj():
    def __init__(self):
        self.pushes: list[Default_Registrar] = []
        self.dotenv_vars: dict[str, str] = {}
        self.hostname_bundles: dict[str, list[tuple[str,str]]] = {}
# Config = DotMap()
Config = Config_Obj()