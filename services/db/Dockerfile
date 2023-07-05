FROM postgres:15.1

ARG VERSION
LABEL version=${VERSION}

HEALTHCHECK \
    --interval=15s \
    --retries=6 \
    --start-period=6s \
    --timeout=6s \
    CMD psql -h localhost -U "${POSTGRES_USER}" -c 'select 1;'  || exit 1
