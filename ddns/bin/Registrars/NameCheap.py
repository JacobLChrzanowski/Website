#!/usr/bin/python3
# import json
# import requests
import logging as log
from .Default import Default_Registrar, DNSRecord, new_dict_exclude_key
from Config.config import Config
from Config.derived_var_helper import get_derived_var

class NameCheap(Default_Registrar):
    """
    api_update_ddns:
    "https://dynamicdns.park-your-domain.com/update?host=@&domain={domain}&password={api_key}&ip={ip}"
    """
    url = "https://dynamicdns.park-your-domain.com/update?host=@&domain={domain}&password={api_key}&ip={ip}"
    def __init__(self, dotenv_varname:str, domains:list[dict[str,str]], start_end_marks: tuple[str, str]) -> None:
        """Config at this point is empty"""
        self.dotenv_varname = dotenv_varname
        self.domains: dict[str, dict[str, str]] = {x['domain']: new_dict_exclude_key(x, 'domain') for x in domains} #type: ignore
        self.start_end_marks = start_end_marks
        if self.dotenv_varname not in Config.dotenv_vars.keys():
            raise self._create_dotenv_KeyError()

    def craft_request(self, api_key: str, domain: str, host_name: str):
        url = self.url.format(domain=domain, api_key=api_key, host_name=host_name)
        # headers = {'content-type': 'application/json'}
        print(url)
        exit()
