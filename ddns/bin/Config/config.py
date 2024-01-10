#!/usr/bin/python3
"""
Only used to share config across application. Should only be declared once, and never re-declared.
"""
# from dotmap import DotMap #type: ignore
# https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Registrars.Default import Default_Registrar, DNSRecord
    from Sources.Default import Default_Source

class Args_Obj():
    def __init__(self, dryrun: bool, verbose: bool, debug: bool):
        self.dryrun = dryrun
        self.verbose = verbose
        self.debug = debug
    def __str__(self):
        return f"dryrun:{self.dryrun} verbose:{self.verbose}"

class Config_Obj():
    def __init__(self):
        self.args: Args_Obj
        self.dotenv_vars: dict[str, str] = {}
        self.pushes: list[Default_Registrar] = []
        self.hostname_bundles: dict[str, list[DNSRecord]] = {}
        self.sources: list[Default_Source]
        self.derived_vars: dict[str, str]
# Config = DotMap()
Config = Config_Obj()