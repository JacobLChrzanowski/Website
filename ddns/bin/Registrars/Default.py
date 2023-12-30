#!/usr/bin/python3
from typing import Any
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from abc import abstractmethod
from config import Config_Obj

class Default_Registrar():
    """
    Template and parent class of other Registrar classes. Basically an interface forp public facing methods.
    Did I just pull some C out of the blue? Maybe. Don't ask. It's a sensitive subject.
    """
    def __init__(self, dotenv_varname:str, domains:list[dict[str,str]], dotenv_vars: dict[str, str], start_end_marks: tuple[str, str]) -> None:
        self.Config: Config_Obj
        self.dotenv_varname = dotenv_varname
        self.domains = domains
        self.dotenv_vars = dotenv_vars
        self.start_end_marks = start_end_marks

    @abstractmethod
    def update(self) -> tuple[str, bool]:
        return True

    def _raise_dotenv_error(self):
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

    def resolve_hostname_pairs_from_bundle(self, hostname: str) -> list[tuple[str, str]]:
        """
        Resolves a list of pairs of hostname/value from a bundle name.
        """
        bundle_name = hostname[1:]
        if bundle_name in self.Config.hostname_bundles:
            return self.Config.hostname_bundles[bundle_name]
        else:
            raise IndexError(f"'{bundle_name}' not present in sites.yaml under key 'hostname_bundles'")
    
    def get_hostname_pair(self, domain: str) -> list[tuple[str, str]]:
        domain_data = self.domains[domain]
        if 'hostname' in domain_data:
            raise NotImplementedError(f"'hostname' is not yet a valid key under 'domains' key. Use bundles instead, for {domain}")
        if 'bundle' in domain_data:
            return self.resolve_hostname_pairs_from_bundle(domain_data['bundle'])
        
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
    >>> print(new_dict)
    {'a': 1, 'c': 3}
    """
    copied_dict = entire_dict.copy()
    del copied_dict[remove_key]
    return copied_dict