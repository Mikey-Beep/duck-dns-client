#!/bin/sh
echo url="https://www.duckdns.org/update?domains=${DOMAIN}&token=${TOKEN}&ip=&verbose=true" | curl -k -o /duck.log -K -
