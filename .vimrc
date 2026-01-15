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
