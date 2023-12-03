# inacanoe.com Prod config

flask-boilerplate
Minimal setup for building a Python API running with Flask and MongoDB, inside Docker Containers. Some more info can be found in [this medium post](https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e).

The Makefile contains all commands required for locally running and testing the system. Run them like, for example, `make dev-up`.

From https://github.com/gabimelo/flask-boilerplate

## Setup
Your .env file in the same folder as the README.md should have the following variables declared:
``` bash
# Consumed in src/__init__.py
LOGGING_LEVEL=debug
POSTGRES_USER=postgres
# Consumed in  docker-ccompose.yml
POSTGRES_PASSWORD="changme"
``````

## Startup
```
> docker compose up
[+] Running 3/0
 ✔ Container inacanoe-prod-postgres_db  Created                                                                                                         0.0s
 ✔ Container inacanoe-prod-redis        Created                                                                                                         0.0s
 ✔ Container inacanoe-prod-web          Created
 ```