FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# 1) Build tools and deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      vim nano build-essential wget libpam0g-dev libselinux1-dev zlib1g-dev \
      pkg-config libssl-dev git ca-certificates \
      openssh-server python3 python3-pip python3-venv supervisor && \
    rm -rf /var/lib/apt/lists/*

# 2) Build vulnerable sudo (1.9.16p2)
ARG SUDO_VERSION=1.9.16p2
WORKDIR /opt
RUN wget -q https://www.sudo.ws/dist/sudo-${SUDO_VERSION}.tar.gz && \
    tar xzf sudo-${SUDO_VERSION}.tar.gz && \
    cd sudo-${SUDO_VERSION} && \
    ./configure --disable-gcrypt --prefix=/usr && \
    make -j"$(nproc)" && \
    make install && \
    cd /opt && rm -rf sudo-${SUDO_VERSION} sudo-${SUDO_VERSION}.tar.gz

# 3) Configure SSH server (and generate host keys)
RUN mkdir -p /var/run/sshd && \
    ssh-keygen -A && \
    (grep -q '^PermitRootLogin' /etc/ssh/sshd_config && \
      sed -i 's/^PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config || \
      echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config) && \
    (grep -q '^PasswordAuthentication' /etc/ssh/sshd_config && \
      sed -i 's/^PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config || \
      echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config)

# 4) Create users joey and davy
RUN useradd -m -s /bin/bash joey && echo "joey:Lf8vw7XJcR02E0bQlogp" | chpasswd && \
    useradd -m -s /bin/bash davy && echo "davy:Je8pw3dFmWRUqeFm3i3l" | chpasswd

# 5) Create user johny with specific shadow entry (base64 hint)
RUN useradd -m -s /bin/bash johny && \
    sed -i 's|^johny:[^:]*:.*|johny:Z29sZGVuX3NuaXRjaAo=:20384:0:99999:7:::|' /etc/shadow

# 6) Prepare webserver dir for davy (MUST exist before copying .bash_history)
RUN mkdir -p /home/davy/webserver && \
    chown -R davy:davy /home/davy/webserver

# 7) Copy notes.txt for joey
COPY --chown=joey:joey joey-files/notes.txt /home/joey/notes.txt

# 8) Copy .bash_history for davy (hint file)
COPY --chown=davy:davy davy-files/.bash_history /home/davy/webserver/.bash_history
RUN chmod 600 /home/davy/webserver/.bash_history

# 9) Copy webserver files
COPY --chown=davy:davy webserver/ /home/davy/webserver/

# 10) Create and setup virtual environment as davy user
USER davy
WORKDIR /home/davy/webserver
RUN python3 -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install flask

# 11) Switch back to root for supervisor setup
USER root

# 12) Configure supervisor to run both services
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 13) Expose ports
EXPOSE 1022 1080

# 14) Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
