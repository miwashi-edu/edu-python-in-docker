FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim git curl ca-certificates build-essential \
    openssh-server \
 && rm -rf /var/lib/apt/lists/*

ARG USER=dev
ARG UID=1000
ARG GID=1000

RUN groupadd -g ${GID} ${USER} \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER} \
 && mkdir -p /var/run/sshd \
 && ssh-keygen -A

# dev:dev
RUN echo "${USER}:${USER}" | chpasswd

# ssh config
RUN sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
 && sed -i 's/^#\?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config \
 && echo "AllowUsers ${USER}" >> /etc/ssh/sshd_config

WORKDIR /work

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r /tmp/requirements-dev.txt

COPY .vimrc /home/${USER}/.vimrc
RUN chown -R ${USER}:${USER} /home/${USER}

EXPOSE 22
CMD ["/usr/sbin/sshd","-D","-e"]
