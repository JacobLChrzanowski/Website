import yaml
from .config import Config
from Registrars.Default import Default_Registrar, DNSRecord
from Registrars.GoDaddy import GoDaddy
from Registrars.NameCheap import NameCheap
from Sources.Default import Default_Source
from Sources.OPNSense import OPNSense

def registrar_preparer(dotenv_vars: dict[str, str]):
    def registrar_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> Default_Registrar:
        """
        self.start_end_marks looks like
        "/home/jacobc/docker/ddns/sites.yaml", line 10, column 3
        """
        values = loader.construct_mapping(node, deep=True)
        start_end_marks = (str(node.start_mark), str(node.end_mark))
        if node.tag == '!GoDaddy':
            return GoDaddy(**values, start_end_marks=start_end_marks) #type: ignore
        if node.tag == '!NameCheap':
            return NameCheap(**values, start_end_marks=start_end_marks) #type: ignore
        raise Exception("Dev Error!!: Unknown Tag")
    return registrar_constructor

def sources_preparer(dotenv_vars: dict[str, str]):
    def sources_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> Default_Source:
        """
        self.start_end_marks looks like
        "/home/jacobc/docker/ddns/sites.yaml", line 10, column 3
        """
        values = loader.construct_mapping(node, deep=True)
        start_end_marks = (str(node.start_mark), str(node.end_mark))
        if node.tag == '!OPNSense':
            return OPNSense(**values, start_end_marks=start_end_marks) #type: ignore
        raise Exception("Dev Error!!: Unknown Tag")
    return sources_constructor


def transform_dns_record_data(bundles: dict[str, list[tuple[str, str, str]]]) -> dict[str, list[DNSRecord]]:
    """
    Transform a dictionary with string keys and lists of tuples to a dictionary with string keys
    and lists of DNSRecord objects.

    Parameters:
    - bundles (dict[str, list[tuple[str, str, str]]]): Input dictionary where keys are strings
      and values are lists of tuples containing three strings each.

    Returns:
    - dict[str, list[DNSRecord]]: Transformed dictionary where keys are strings and values
      are lists of DNSRecord objects.
    ```
    """
    output: dict[str, list[DNSRecord]] = {}
    for key, records in bundles.items():
        new_records: list[DNSRecord] =  []
        for record in records:
            new_records.append(DNSRecord(record[0], record[1], record[2]))
        output[key] = new_records
    return output

def get_loader(dotenv_vars: dict[str, str]) -> type[yaml.SafeLoader]:
    """
    Gets the yaml SafeLoader,
    Applies custom constructors to loader class
    Returns it for use in yaml.load(loader=<thi)

    I think FullLoader would have been fine, online it seems people think so. But we're playing it safe here.

    loader. or yaml. add_implicit_resolver must be called on the loader variable, and not on just the yaml class.
    As far as I can tell, pyyaml does not add any custom implicit resolvers to the SafeLoader loader if they are called from the library. If you want to add custom resolvers to SafeLoader, you must call the function on that loader.
    https://github.com/yaml/pyyaml/blob/main/lib/yaml/__init__.py :: add_implicit_resolver
    """
    loader = yaml.SafeLoader
    loader.add_constructor('!GoDaddy', registrar_preparer(dotenv_vars))
    loader.add_constructor('!NameCheap', registrar_preparer(dotenv_vars))
    loader.add_constructor('!OPNSense', sources_preparer(dotenv_vars))
    return loader

def get_yaml_config(yaml_path: str, dotenv_vars: dict[str, str]) -> None:
    contents = yaml.load(open(yaml_path),
                         Loader=get_loader(dotenv_vars))
    Config.pushes = contents['pushes']
    Config.hostname_bundles = transform_dns_record_data(contents['hostname_bundles'])
    Config.sources = contents['sources']
    if contents['derived_vars']:
        Config.derived_vars = contents['derived_vars']
    else:
        Config.derived_vars = {}