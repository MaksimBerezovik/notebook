FROM nginx:1.24.0-alpine

ARG VERSION
LABEL version=${VERSION}

RUN install -m 0755 -d /localhost-certs/
COPY ./certs/*.crt /localhost-certs/
COPY ./certs/*.key /localhost-certs/

COPY ./conf.d/default.conf /etc/nginx/conf.d/
COPY ./conf.d/m-pt1-63-23.local/*.conf /etc/nginx/conf.d/

ARG PORT_HTTP
EXPOSE ${PORT_HTTP}
RUN sed -e "s+PORT_HTTP+${PORT_HTTP}+" -i.bak /etc/nginx/conf.d/*.conf

ARG PORT_SSL_HTTPS
EXPOSE ${PORT_SSL_HTTPS}
RUN sed -e "s+PORT_SSL_HTTPS+${PORT_SSL_HTTPS}+" -i.bak /etc/nginx/conf.d/*.conf
