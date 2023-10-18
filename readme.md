# Installation

## Getting a domain and token

[DuckDNS](https://www.duckdns.org/)

## Starting the container

``` bash
docker run --name duckdns --restart=always -e DOMAIN={DOMAIN_NAME} -e TOKEN={TOKEN} -d duckdns
```
