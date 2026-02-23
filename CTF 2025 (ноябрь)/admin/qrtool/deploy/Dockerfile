FROM alpine:3.19
WORKDIR /app

RUN apk add --no-cache libqrencode-tools iptables

COPY --chmod=644 src/ipt /root/ipt
COPY --chmod=755 src/qrgen /usr/local/bin/qrgen

EXPOSE 23

CMD /sbin/iptables-restore < /root/ipt && \
    su guest -s /bin/sh -c '/usr/bin/nc -z -lk -p 23 -e /usr/local/bin/qrgen'
