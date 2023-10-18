FROM alpine:latest
COPY duckdns.sh /etc/periodic/15min/duckdns.sh
RUN apk add --no-cache curl && \
    chmod +x /etc/periodic/15min/duckdns.sh
CMD ["crond", "-f"]
