#!/usr/bin/python3
from Registrars.Default import Default_Registrar, new_dict_exclude_key
from config import Config, Config_Obj

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
                 dotenv_vars:           dict[str, str],
                 start_end_marks:       tuple[str, str]
                ) -> None:
        """Config at this point is empty"""
        self.Config: Config_Obj = Config
        self.dotenv_varname = dotenv_varname
        self.domains: dict[str, str]  = {x['domain']: new_dict_exclude_key(x, 'domain') for x in domains} #type: ignore
        self.dotenv_vars = dotenv_vars
        self.start_end_marks = start_end_marks
        if self.dotenv_varname not in self.dotenv_vars.keys():
            raise self._raise_dotenv_error()

    def update(self) -> tuple[str, bool]:
        for domain in self.domains.keys():
            hostname_pairs = self.get_hostname_pair(domain)
            api_key: str = Config.dotenv_vars[self.dotenv_varname]

            for hostname_pair in hostname_pairs:
                self.craft_request(api_key, domain, hostname_pair)

        return ('a', False)

    def craft_request(self, api_key: str, domain: str, hostname_pair:tuple[str, str]):
        url = self.url.format(domain=domain, record_type=hostname_pair[0], hostname=hostname_pair[1])
        headers = {'content-type': 'application/json'}
        payload = {'some': 'data'}
        print(f"{url} {headers} {payload}")
        # exit()

        
        # r = requests.post(url, data=json.dumps(payload), headers=headers)

