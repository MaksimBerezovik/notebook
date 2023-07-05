FROM certbot/certbot:v2.5.0

ARG VERSION
LABEL version=${VERSION}

COPY ./entrypoint.sh .

ENV RENEW_COOLDOWN=43200

ENTRYPOINT ["./entrypoint.sh"]
