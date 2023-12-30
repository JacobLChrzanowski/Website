#!/usr/bin/python3

import os
import yaml
# from dotmap import DotMap #type: ignore
from dotenv import dotenv_values
from config import Config
from Registrars.Default import Default_Registrar
from Registrars.GoDaddy import GoDaddy
from Registrars.NameCheap import NameCheap

def registrar_preparer(dotenv_vars: dict[str, str]):
    def registrar_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> Default_Registrar:
        """
        self.start_end_marks looks like
        "/home/jacobc/docker/ddns/sites.yaml", line 10, column 3
        """
        values = loader.construct_mapping(node, deep=True)
        start_end_marks = (str(node.start_mark), str(node.end_mark))

        if node.tag == '!GoDaddy':
            return GoDaddy(**values, dotenv_vars=dotenv_vars, start_end_marks=start_end_marks) #type: ignore
        if node.tag == '!NameCheap':
            return NameCheap(**values, dotenv_vars=dotenv_vars, start_end_marks=start_end_marks) #type: ignore
        raise Exception("Dev Erro!!: Unknown Tag")
    return registrar_constructor

def get_loader(dotenv_vars: dict[str, str]) -> type[yaml.SafeLoader]:
    loader = yaml.SafeLoader
    loader.add_constructor('!GoDaddy', registrar_preparer(dotenv_vars))
    loader.add_constructor('!NameCheap', registrar_preparer(dotenv_vars))
    return loader

def get_yaml_config(yaml_path: str, dotenv_vars: dict[str, str]) -> None:
    contents = yaml.load(open(yaml_path), Loader=get_loader(dotenv_vars))
    # with open(yaml_path, "r") as f:
    #     try:
    #         contents = yaml.load(f, Loader=get_loader())
    #     except yaml.YAMLError as exc:
    #         raise exc
    Config.pushes = contents['pushes']
    Config.hostname_bundles = contents['hostname_bundles']
    # dotmap = DotMap(contents)
    # return dotmap

def get_dotenv_vars(dotenv_dir: str) -> dict[str, str]:
    dotenv_filepath = os.path.join(dotenv_dir, '.env')
    dotenv_vars = dict(dotenv_values(dotenv_filepath))

    if len(dotenv_vars.keys()) == 0:
        raise(Exception("No .env vars?"))

    return dotenv_vars #type: ignore # fixed in Python3.10

def get_config(yaml_path: str, dotenv_dir: str) -> None:
    Config.dotenv_vars = get_dotenv_vars(dotenv_dir) #type: ignore
    get_yaml_config(yaml_path, Config.dotenv_vars)
    # yaml_config.dotenv_vars = dotenv_vars

    # return yaml_config

