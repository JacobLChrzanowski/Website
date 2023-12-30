#!/usr/bin/python3

import os
# from dotmap import DotMap #type: ignore
import config_helper as conf
from config import Config
from Registrars.Default import Default_Registrar
DDNS_FOLDER = os.path.dirname(os.path.dirname(__file__))
CONFIG_FOLDER = os.path.join(DDNS_FOLDER, 'config')
SITES_PATH = os.path.join(DDNS_FOLDER, 'sites.yaml')

if __name__ == '__main__':
    # Config.update(conf.get_config(yaml_path=SITES_PATH, dotenv_dir=DDNS_FOLDER))
    conf.get_config(yaml_path=SITES_PATH, dotenv_dir=DDNS_FOLDER)
    print(Config.hostname_bundles)
    Config.pushes[0].update()
    exit()
    
    print(f"in main, printing Config var: {Config}")
    registrar: Default_Registrar = Config.pushes[0]
    registrar.update()

    exit()
    import code, readline
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()