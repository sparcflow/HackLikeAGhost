#!/bin/bash

sed -i /etc/nginx/conf.d/*.conf -e "s/__DOMAIN__/$DOMAIN/g"
sed -i /etc/nginx/conf.d/*.conf -e "s/__IP__/$C2IP/g"

/scripts/entrypoint.sh