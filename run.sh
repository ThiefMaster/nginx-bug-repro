#!/bin/sh

nginx -c /app/nginx.conf -e /dev/stdout &
flask run -p 12345 -h 0.0.0.0
