#!/usr/bin/python3
# Entry Point for Config Folder

from .config import Config, Args_Obj
from .dotenv_helper import get_dotenv_vars
from .yaml_helper import get_yaml_config, update_hostname_bundles
from .derived_var_helper import get_derived_vars
# from Registrars.Default import Default_Registrar
# from Registrars.GoDaddy import GoDaddy
# from Registrars.NameCheap import NameCheap
# from Sources.Default import Default_Source
# from Sources.OPNSense import OPNSense

def get_config(etc_folder: str, yaml_path: str, args: Args_Obj) -> None:
    """
    Functional entrypoint to this file.
    """
    Config.dotenv_vars = get_dotenv_vars(etc_folder) #type: ignore
    Config.args = args
    get_yaml_config(yaml_path, Config.dotenv_vars)
    get_derived_vars()
    update_hostname_bundles()


