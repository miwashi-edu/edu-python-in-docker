# edu-python-in-docker

## Instructions 

```bash
mkdir pyvim && cd pyvim
```

### Create Docker file

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

### rewuirements-dev.txt

```bash
cat <<'EOF' > requirements-dev.txt
black
ruff
pytest
ipython
EOF
```

### .vimrc

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





