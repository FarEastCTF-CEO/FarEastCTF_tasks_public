FROM alpine:3.19
WORKDIR /app

RUN apk add --no-cache openssh-server iptables

RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N "" && \
    ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N "" && \
    ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""

RUN echo -e "PubkeyAuthentication no\nPermitTTY no\nPrintMotd no\nSubsystem sftp /bin/false" > /etc/ssh/sshd_config.d/99-custom.conf

ARG SSH_USER
ARG SSH_USER_PASS
ARG FLAG

RUN echo "$FLAG" > ./flag && \
    addgroup "$SSH_USER" && \
    adduser -h /app -s /bin/shell -H -D -G "$SSH_USER" "$SSH_USER" && \
    echo "$SSH_USER:$SSH_USER_PASS" | chpasswd

COPY --chmod=644 ipt /root/ipt
COPY --chmod=755 shell /bin/shell

EXPOSE 22

CMD iptables-restore < /root/ipt && \
    /usr/sbin/sshd -D -e
