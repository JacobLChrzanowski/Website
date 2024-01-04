#!/usr/bin/python3
from .Default import Default_Registrar
from Config.config import Config, Config_Obj

class NameCheap(Default_Registrar):
    """
    api_update_ddns:
    "https://dynamicdns.park-your-domain.com/update?host=@&domain={domain}&password={api_key}&ip={ip}"
    """
    url = "https://dynamicdns.park-your-domain.com/update?host=@&domain={domain}&password={api_key}&ip={ip}"
    def __init__(self, dotenv_varname:str, domains:list[dict[str,str]], start_end_marks: tuple[str, str]) -> None:
        
        self.Config: Config_Obj = Config
        self.dotenv_varname = dotenv_varname
        self.domains = domains
        pass

    def craft_request(self, api_key: str, domain: str, host_name: str):
        url = self.url.format(domain=domain, api_key=api_key, host_name=host_name)
        # headers = {'content-type': 'application/json'}
        print(url)
        exit()
