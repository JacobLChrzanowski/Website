#!python3
import json
import requests
import logging as log
from .Default import Default_Registrar, DNSRecord, new_dict_exclude_key
from Config.config import Config, Config_Obj
from Config.derived_var_helper import get_derived_var

class GoDaddy(Default_Registrar):
    """
    curl -s -X PUT 
    "https://api.godaddy.com/v1/domains/${mydomain}/records/A/${recordname}"
    -H "Authorization: sso-key ${gdapikey}"
    -H "Content-Type: application/json"
    -d "[{\"data\": \"${myip}\"}]"
    """
    url = "https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{hostname}"
    def __init__(self, dotenv_varname:  str,
                 domains:               list[dict[str, str]],
                 start_end_marks:       tuple[str, str]
                ) -> None:
        """Config at this point is empty"""
        self.Config: Config_Obj = Config
        self.dotenv_varname = dotenv_varname
        self.domains: dict[str, str] = {x['domain']: new_dict_exclude_key(x, 'domain') for x in domains} #type: ignore
        self.start_end_marks = start_end_marks
        if self.dotenv_varname not in Config.dotenv_vars.keys():
            raise self._create_dotenv_KeyError()

    def update(self) -> tuple[str, bool]:
        for domain in self.domains.keys():
            hostname_pairs = self.get_dns_records_for_domain(domain)
            api_key: str = Config.dotenv_vars[self.dotenv_varname]

            for hostname_pair in hostname_pairs:
                self.craft_request(api_key, domain, hostname_pair)

        return ('a', False)

    def craft_request(self, api_key: str, domain: str, hostname_pair:tuple[str, str, str]):
        dns_entry_value = get_derived_var(hostname_pair[2])
        if dns_entry_value is None:
            raise KeyError(f"'{hostname_pair[2]}' is not present in derived values!")
        dns_record = DNSRecord(hostname_pair[0], hostname_pair[1], hostname_pair[2])
        
        url = self.url.format(domain=domain, record_type=hostname_pair[0], hostname=hostname_pair[1])
        api_keyA, api_keyB = api_key.split(':')
        headers = {'content-type': 'application/json',
                   'Authorization': f'sso-key {api_keyA}:{api_keyB}'
        }
        payload = [{'data': dns_entry_value}]


        if not Config.args.dryrun:
            r = requests.put(url, data=json.dumps(payload), headers=headers)
            log.debug(r)
            if r.status_code == 200:
                return True
        else:
            log.debug(f"{url} {headers} {payload}")

