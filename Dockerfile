FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim git curl ca-certificates build-essential \
 && rm -rf /var/lib/apt/lists/*

ARG USER=dev
ARG UID=1000
ARG GID=1000

RUN groupadd -g ${GID} ${USER} \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER}

WORKDIR /work

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r /tmp/requirements-dev.txt

COPY .vimrc /home/${USER}/.vimrc
RUN chown -R ${USER}:${USER} /home/${USER}

USER ${USER}
CMD ["bash"]
