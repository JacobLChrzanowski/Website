#!/usr/bin/python3

import os
import yaml
from dotmap import DotMap #type: ignore
from dotenv import dotenv_values
from Registrars.GoDaddy import GoDaddy
from Registrars.NameCheap import NameCheap
REPO_FOLDER = os.path.dirname(os.path.dirname(__file__))
CONFIG_FOLDER = os.path.join(REPO_FOLDER, 'config')
SITES_PATH = os.path.join(REPO_FOLDER,'sites.yaml')

def godaddy_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> GoDaddy:
    # print(loader)
    # print(node)
    # exit()
    # values = loader.construct_mapping(node)#, deep=True)
    # print(type(node))
    # return GoDaddy(**values)
    if loader = 
    return GoDaddy()

def get_loader() -> type[yaml.SafeLoader]:
    loader = yaml.SafeLoader
    loader.add_constructor('!GoDaddy', registrar_constructor)
    loader.add_constructor('!GoDaddy', registrar_constructor)
    return loader

def getYamlConfig(yaml_path: str ) -> DotMap:
    contents = yaml.load(open(yaml_path), Loader=get_loader())
    # with open(yaml_path, "r") as f:
    #     try:
    #         contents = yaml.load(f, Loader=get_loader())
    #     except yaml.YAMLError as exc:
    #         raise exc
    dotmap = DotMap(contents)
    return dotmap

def getDotEnvVars() -> dict[str, str]:
    dotenv_filepath = os.path.join(REPO_FOLDER,'.env')
    dotenv_vars = dotenv_values(dotenv_filepath)
    if len(dotenv_vars.keys()) == 0:
        raise(Exception("No .env vars?"))
    return dotenv_vars #type: ignore

if __name__ == '__main__':
    config = getYamlConfig(SITES_PATH)
    print(config)
    dotEnvVars = getDotEnvVars()
    print(dotEnvVars.keys())
    exit()
    import code, readline
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()