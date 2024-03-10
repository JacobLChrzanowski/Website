# My website(s) and accompanying tools

Folders:
- ddns: dynamic dns client
- inacanoe: inacanoe.com source code

## required software
- docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
- postgresql-client

## notes
Nginx config is separate.
In the future, each site will have its own section that defines how the nginx server on the host should point traffic at the container(s)
Docker is used mainly for ease of deployment and cleanup of data. I don't intend to need to multi-box any of these sites.