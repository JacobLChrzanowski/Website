
class GoDaddy():
    """
    curl -s -X PUT 
    "https://api.godaddy.com/v1/domains/${mydomain}/records/A/${recordname}"
    -H "Authorization: sso-key ${gdapikey}"
    -H "Content-Type: application/json"
    -d "[{\"data\": \"${myip}\"}]"
    """
    url = "https://api.godaddy.com/v1/domains/${domain}/records/A/${host_name}"
    def __init__(self):
        pass

    def craft_request(self, api_key, domain, host_name):
        url = self.url.format(domain=domain, host_name=host_name)
        headers = {'content-type': 'application/json'}
        print(url)
        exit()
