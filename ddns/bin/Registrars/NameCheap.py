

class NameCheap():
    """
    api_update_ddns:
    "https://dynamicdns.park-your-domain.com/update?host=@&domain={domain}&password={api_key}&ip={ip}"
    """
    url = "https://dynamicdns.park-your-domain.com/update?host=@&domain={domain}&password={api_key}&ip={ip}"
    def __init__(self):
        pass

    def craft_request(self, api_key: str, domain: str, host_name: str):
        url = self.url.format(domain=domain, api_key=api_key, host_name=host_name)
        # headers = {'content-type': 'application/json'}
        print(url)
        exit()
