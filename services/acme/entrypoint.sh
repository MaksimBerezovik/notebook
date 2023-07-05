#!/bin/sh

trap exit TERM

while :; do
  sleep 1
  certbot renew
  sleep "${RENEW_COOLDOWN:-43200}" &
  wait ${!}
done
