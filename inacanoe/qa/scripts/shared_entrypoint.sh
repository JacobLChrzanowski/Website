#!/bin/sh

if [ "$1" = "qa" ]; then
    /usr/bin/python3 -m flask --app "web_src.app:create_app()" run \
        --host=0.0.0.0 \
        --port 5010 \
        --debug
elif [ "$1" = "prod" ]; then
    /usr/sbin/uwsgi --ini /etc/uwsgi/uwsgi.ini --die-on-term
else
    echo "Usage: $0 [qa|prod]"
    exit 1
fi