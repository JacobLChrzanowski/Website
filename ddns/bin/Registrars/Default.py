#!/usr/bin/python3
from typing import Any
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from abc import abstractmethod
from Config.config import Config_Obj

class DNSRecord():
    def __init__(self, record_type: str, record_name: str, data: str, ttl: int = 600):
        """
        record_type: A, NS, MX, TXT, etc
        record_name: @, a string, etc
        data: value associated with the record
        """
        self.record_type = record_type
        self.record_name = record_name
        self.data = data
        self.ttl = ttl

    def __str__(self):
        return f"DNSRecord(record_type={self.record_type}, ttl={self.ttl}, data={self.data})"

class Default_Registrar():
    """
    Template and parent class of other Registrar classes. Basically an interface forp public facing methods.
    Did I just pull some C out of the blue? Maybe. Don't ask. It's a sensitive subject.
    """
    def __init__(self,
                 dotenv_varname:str,
                 domains:list[dict[str,str]],
                 start_end_marks:
                 tuple[str, str]
                ) -> None:
        self.Config: Config_Obj
        self.dotenv_varname = dotenv_varname
        self.domains: dict[str, str] = {x['domain']: new_dict_exclude_key(x, 'domain') for x in domains} #type: ignore
        self.start_end_marks = start_end_marks

    @abstractmethod
    def update(self) -> tuple[str, bool]:
        return True

    def _create_dotenv_KeyError(self):
        error = KeyError(f"The .env is missing a defined key in pushes/!{self.__class__.__name__} "
                 f"- you should fix this in {self._fmt_file_from_start_end_marks()} between lines {self._fmt_start_mark()} and {self._fmt_end_mark()}")
        return error

    def _fmt_start_end_marks(self, start_or_end_mark : str) -> int:
        """
        self.start_end_marks looks like
        "/home/jacobc/docker/ddns/sites.yaml", line 10, column 3
        """
        return int(start_or_end_mark.split(',')[1].strip().split(' ')[1])
    def _fmt_start_mark(self) -> int:
        return self._fmt_start_end_marks(self.start_end_marks[0])
    def _fmt_end_mark(self) -> int:
        return self._fmt_start_end_marks(self.start_end_marks[1])
    def _fmt_file_from_start_end_marks(self) -> str:
        return self.start_end_marks[0].split(',')[0].split('"')[1]

    def _get_DNSRecords_by_bundlename(self, bundlename: str) -> list[DNSRecord]:
        """
        Resolves a list of pairs of hostname/value from a bundle name.
        If you give it "!default" it will return the list under hostname_bundles > default
        """
        bundle_name = bundlename[1:]
        if bundle_name in self.Config.hostname_bundles:
            return self.Config.hostname_bundles[bundle_name]
        else:
            raise IndexError(f"'{bundle_name}' not present in sites.yaml under key 'hostname_bundles'")

    # def get_hostname_pair(self, domain: str) -> list[tuple[str, str, str]]:
    def get_dns_records_for_domain(self, domain: str) -> list[tuple[str, str, str]]:
        """returns a list of DNSRecord Objects based on the provided domain for this current object
        This involves looking up the bundle name in Config.hostname_bundles
        """
        domain_data = self.domains[domain]
        if 'hostname' in domain_data:
            raise NotImplementedError(f"'hostname' is not yet a valid key under 'domains' key. Use bundles instead, for {domain}")
        if 'bundle' in domain_data:
            return self._get_DNSRecords_by_bundlename(domain_data['bundle'])

        raise ValueError(f"Neither 'hostname' nor 'bundle' key are present under 'domains' key for domain {domain}")



def new_dict_exclude_key(entire_dict: dict[Any, Any], remove_key: Any) -> dict[Any, Any]:
    """
    Create a new dictionary by excluding a specified key and its associated value.

    Parameters:
    - original_dict (dict): The input dictionary.
    - key_to_exclude (str): The key to be excluded from the dictionary.

    Returns:
    - dict: A new dictionary without the specified key and its associated value.

    Example:
    >>> input_dict = {'a': 1, 'b': 2, 'c': 3}
    >>> new_dict = exclude_key(input_dict, 'b')
    {'a': 1, 'c': 3}
    """
    copied_dict = entire_dict.copy()
    del copied_dict[remove_key]
    return copied_dict