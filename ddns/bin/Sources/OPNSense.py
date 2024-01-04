#
import re
import json
import requests
import logging as log
from .Default import Default_Source
from Config.config import Config
from Config.derived_var_helper import get_derived_var, set_derived_var
from Config.dotenv_helper import get as dotenv_get

class OPNSense(Default_Source):
    # Preferred url, but OPNSense does not present an access group for this api
    # url = "https://{host}/api/diagnostics/interface/getinterfaceconfig"
    url = "https://{host}/api/diagnostics/interface/getInterfaceStatistics/lan"

    def __init__(self,
                 dotenv_key:str,
                 dotenv_secret: str,
                 host: str,
                 exports: list[str],
                 verify_ssl: bool,
                 start_end_marks: tuple[str, str] = ('0', '0')
                ) -> None:
        self.start_end_marks = start_end_marks
        self.verify_ssl = verify_ssl
        self.exports = exports
        self.host = host
        self.secret = dotenv_get(dotenv_secret, self._create_dotenv_KeyError())
        self.key = dotenv_get(dotenv_key, self._create_dotenv_KeyError())

    def send_get(self,
                 url: str,
                 headers: dict[str, str],
                 auth: tuple[str, str],
                 acceptable_status_codes: tuple[int]
                 ) -> dict[str, dict[str, str]]:
        """
        """
        session = requests.Session()
        session.auth = auth
        req = session.get(url, headers=headers, verify=self.verify_ssl)
        if req.status_code not in acceptable_status_codes:
            raise Exception(f"{self.__class__.__name__} failed to retrieve data from host.")
        try:
            return req.json()
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"{self.__class__.__name__} expected json but did not recieve parsable json.\n{e}")
        
    def regex_check_for_ipv4(self, string: str) -> bool:
        re_ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        re_search = re.search(re_ipv4_pattern, string)
        if re_search is None:
            return False
        if len(re_search.group()) == 0:
            return False
        return True

    def _get_ip(self, req_content: dict[str, dict[str, str]]) -> str:
        if 'statistics' not in req_content:
            raise self._create_bad_response_exception(req_content)
        statistics = req_content['statistics']
        statistics_keys = statistics.keys()

        found_address = ""
        for key in statistics_keys:
            if '[wan]' not in key:
                continue
            if not self.regex_check_for_ipv4(key):
                continue
            if 'address' not in statistics[key]:
                continue
            found_address = statistics[key]['address'] #type: ignore
            break
        if not found_address:
            raise self._create_bad_response_exception(req_content)
        return found_address

    def _create_bad_response_exception(self, content: dict[str, dict[str, str]]) -> Exception:
        return Exception(f"{self.__class__.__name__} found bad response:\n{content}")

    def get_function_from_exported_varname(self, varname: str):
        if varname == 'public_ip':
            return self.get_public_ip
        else:
            raise Exception(f"{self.__class__.__name__} attempts to export a varname wth no associated internal export function.")

    def obtain_state(self) -> None:
        for key in self.exports:
            if get_derived_var(key) is not None:
                continue
            self.get_function_from_exported_varname(key)(key)


    def get_public_ip(self, key: str) -> None:
        url = self.url.format(host=self.host)
        headers = {'Accept-Encoding': 'gzip, deflate, br'}
        auth = (self.key, self.secret)

        if not Config.args.dryrun:
            content = self.send_get(url, headers, auth, (200,))
            found_address = self._get_ip(content)
        else:
            log.debug(f"{url} {headers}") #TODO: log debug and improve how it's reported
            found_address = '0.0.0.0'

        set_derived_var(key, found_address)
