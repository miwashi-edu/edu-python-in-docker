# edu-python-in-docker

> Tutorial creates a python machine in docker for exploratory coding.
> The machine can be restarted with `docker compose run --rm pyvim`
> To exit the machine, use Ctrl-d
> The -rm removes the image after EOF (Ctrl-d)
> If you want to keep it, remove the -rm argument, then login with:
> 1. `docker start pyvim`
> 2. `docker exec -it pyvim bash`


## Instructions 

> Use the copy button in git, then just paste the code into bash.
> `cat << 'EOF' > filename ... EOF` is called heredoc, and writes a file if pasted into bash terminal.

### If not already created, create iotnet docker network.

```bash
docker network create \
  --driver bridge \
  --subnet 192.168.2.0/24 \
  --gateway 192.168.2.1 \
  iotnet
```

### Create project directory

```bash
mkdir pyvim && cd pyvim
```

### Create Docker file

> Dockerfile is used to create the image

```bash
cat <<'EOF' > Dockerfile
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
EOF
```

### Create requirements-dev.txt

> Edit this to add python libraries you need.

```bash
cat <<'EOF' > requirements-dev.txt
black
ruff
pytest
ipython
EOF
```

### docker-compose.yml

> Docker compose is a more advanced way to create containers

```bash
cat <<'EOF' > docker-compose.yml
services:
  pyvim:
    build: .
    volumes:
      - ./:/work
    working_dir: /work
    tty: true
    stdin_open: true
    networks:
      - iotnet

networks:
  iotnet:
    external: true
EOF
```

### Configure VIM for Python use.

```bash
cat <<'EOF' > .vimrc
set nocompatible
syntax on
filetype plugin indent on

set number
set relativenumber
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent
set hidden
set ignorecase
set smartcase
set incsearch
set hlsearch

let mapleader=" "

nnoremap <leader>w :w<CR>
nnoremap <leader>r :w<CR>:!python %<CR>
nnoremap <leader>b :w<CR>:!black -q %<CR>
nnoremap <leader>f :w<CR>:!ruff check %<CR>
EOF
```

### .gitignore

```bash
cat <<'EOF' > .gitignore
__pycache__/
.pytest_cache/
*.pyc
EOF
```

## Sample Source

```bash
mkdir -p src

cat <<'EOF' > src/main.py
def add(a, b):
    return a + b

if __name__ == "__main__":
    print(add(2, 3))
EOF
```

## Build and Start the Container

```bash
docker compose build
docker compose run --rm pyvim # This will log you in to bash in the container
```

## In container

### Edit Script

```bash
vim src/main.py
```

### Run Script

```bash
python src/main.py
```


### Exit container

```bash
Ctrl-D
```










