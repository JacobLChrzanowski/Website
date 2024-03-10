# ddns client
This is a dynamic dns client.
It is unfinished in the sense that deploying it via a cron job would make unneccessary calls to domain registrars, becuase it does not check whether an IP has changed since the last time it ran. But it does work in every other sense.
\
I wrote it because the dynamic dns client in OPNSense did not support NameCheap, and I got mad, and wrote this extensible one instead.

## config
Configuration is stored in etc/
### etc/sites.yaml
etc/sites.yaml makes references to variable names which need to be set in etc/.env
\
TODO: more info

### etc/.env (you must create this file)
Standard .env file that can be read by python's **`dotenv`** library
```
apikey_godaddy=""
apikey_namecheap_inacanoe.com=""
apikey_opnsense_key=""
apikey_opnsense_secret=""
```