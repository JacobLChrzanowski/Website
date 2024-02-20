#!/usr/bin/python3
import json
import requests
import logging as log
from .Default import Default_Registrar, DNSRecord, new_dict_exclude_key
from Config.config import Config

class NameCheap(Default_Registrar):
    """
    api_update_ddns:
    https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-to-dynamically-update-the-hosts-ip-with-an-https-request/
    """
    url = "https://dynamicdns.park-your-domain.com/update?host={record_name}&domain={domain}&password={api_key}&ip={ip}"
    def __init__(self, dotenv_varname:str, domains:list[dict[str,str]], start_end_marks: tuple[str, str]) -> None:
        """Config at this point is empty"""
        self.dotenv_varname = dotenv_varname
        self.domains: dict[str, dict[str, str]] = {x['domain']: new_dict_exclude_key(x, 'domain') for x in domains} #type: ignore
        self.start_end_marks = start_end_marks
        if self.dotenv_varname not in Config.dotenv_vars.keys():
            raise self._create_dotenv_KeyError()

    def update(self) -> tuple[str, bool]:
        for domain in self.domains.keys():
            dns_records = self.get_dns_records_for_domain(domain)
            api_key: str = Config.dotenv_vars[self.dotenv_varname]

            for record in dns_records:
                self.craft_request(api_key, domain, record)

        return ('a', False) #TODO return results

    def craft_request(self, api_key: str, domain: str, dns_record: DNSRecord):
        url = self.url.format(domain=domain, api_key=api_key, record_name=dns_record.record_name, ip=dns_record.data)
        headers = {'content-type': 'application/json'}
        # payload = [{'data': dns_record.data}]

        if not Config.args.dryrun:
            r = requests.get(url, headers=headers)
            log.debug(r)
            if r.status_code == 200:
                return True
            else:
                log.debug(r.content)
        else:
            log.debug(f"{url.replace(api_key, 'xxx')} {headers}")
