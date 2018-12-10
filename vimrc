set langmenu=en_US
let mapleader = " "
nnoremap <space> <nop>
let $LANG = 'en_US'
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim

nnoremap <leader>w :wa<CR>

" syntastic
execute pathogen#infect()

" ctrl n+p to switch buffers
nnoremap <C-n> :bnext<CR>
nnoremap <C-p> :bprevious<CR>

" make find command look in current folder too
set path+=**

hi statusline ctermfg=9 ctermbg=15
" Formats the statusline
set statusline=%f                           " file name
set statusline+=\ 
set statusline+=[%{strlen(&fenc)?&fenc:'none'}, "file encoding
set statusline+=%{&ff}] "file format
set statusline+=%y      "filetype
set statusline+=%h      "help file flag
set statusline+=%m      "modified flag
set statusline+=%r      "read only flag

" Puts in the current git status
" if count(g:pathogen_disabled, 'Fugitive') < 1   
"  set statusline+=%{fugitive#statusline()}
" endif

" Puts in syntastic warnings
"if count(g:pathogen_disabled, 'Syntastic') < 1  
  set statusline+=%#warningmsg#
  set statusline+=%{SyntasticStatuslineFlag()}
  set statusline+=%*
" endif

set statusline+=\ %=                        " align left
" set statusline+=Line:%l/%L[%p%%]            " line X of Y [percent of file]
set statusline+=ln:%l/%L                    " line X of Y
set statusline+=\ Col:%c                    " current column
set statusline+=\ Buf:%n                    " Buffer number
" set statusline+=\ [%b][0x%B]\               " ASCII and byte code under cursor

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
let g:syntastic_lua_checkers = ["luac", "luacheck"]

if has('gui_running')
    set background=light
    colorscheme solarized
else
    " set background=light
    " colorscheme solarized
endif

:set guioptions-=m  "remove menu bar
:set guioptions-=T  "remove toolbar
:set guioptions-=r  "remove right-hand scroll bar
:set guioptions-=L  "remove left-hand scroll bar

" make , reapeat the quick macro
nnoremap , @q

set history=50
set ruler         " show the cursor position all the time
set showcmd       " display incomplete commands
set incsearch     " do incremental searching
set laststatus=2  " Always display the status line
set autowrite     " Automatically :write before running commands

" Softtabs, 2 spaces
set tabstop=2
set shiftwidth=2
set softtabstop=2
set shiftround
set expandtab

function! SetPythonSpacing()
  setlocal tabstop=4
  setlocal shiftwidth=4
  setlocal softtabstop=4
endfunction

autocmd FileType python call SetPythonSpacing()

" Treat <li> and <p> tags like the block tags they are
let g:html_indent_tags = 'li\|p'
syntax on

filetype indent on

" for python files, draw line at margin
autocmd FileType python setlocal colorcolumn=79 | highlight ColorColumn ctermbg=White guibg=orange

" linenumbers
set number
set numberwidth=4

" highlight current line
" Enable CursorLine
set cursorline

" Default Colors for CursorLine
highlight clear CursorLine
highlight CursorLine ctermbg=White guibg=#e4e4e4

" autocmd! " remove ALL autocommands

" Relative line numbers
" http://jeffkreeftmeijer.com/2012/relative-line-numbers-in-vim-for-super-fast-movement/

set rnu

function! NumberToggle()
  if(&relativenumber == 1)
    set nornu
  else
    set rnu
  endif
endfunc

nnoremap <C-n> :call NumberToggle()<cr>

:au FocusLost * :set nornu
:au FocusGained * :set rnu

autocmd InsertEnter * :set nornu
autocmd InsertLeave * :set rnu


" fix slow escape escape
:set timeout timeoutlen=10

" https://stackoverflow.com/a/11993928/180307
nnoremap <leader>c "_c
nnoremap <leader>d "_d
xnoremap <leader>d "_d
xnoremap <leader>p "_dP

" move lines or blocks up/down with alt+movment
nnoremap <C-j> :m .+1<CR>==
nnoremap <C-k> :m .-2<CR>==
inoremap <C-j> <Esc>:m .+1<CR>==gi
inoremap <C-k> <Esc>:m .-2<CR>==gi
vnoremap <C-j> :m '>+1<CR>gv=gv
vnoremap <C-k> :m '<-2<CR>gv=gv

" make ctrl-y and ctrl-p copy and paste from system clipboard
nnoremap <C-y> "+y
nnoremap <C-p> "+p

" make enter in normal enter a new line
nmap <CR> o<Esc>
