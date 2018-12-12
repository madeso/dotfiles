" ============================================================================
" Global settings:
" ============================================================================

set langmenu=en_US
let $LANG = 'en_US'
set encoding=utf-8

" let leader be the space
let mapleader = " "
nnoremap <space> <nop>

" make vim less vi compatible
set nocompatible

" make vim more secure by disabling vim commands at the start of files
set modelines=0

" remap arrow keys to resize in normal mode, disable elsewhere
nnoremap <Left> :vertical resize -1<CR>
nnoremap <Right> :vertical resize +1<CR>
nnoremap <Up> :resize -1<CR>
nnoremap <Down> :resize +1<CR>
inoremap <up> <nop>
inoremap <down> <nop>
inoremap <left> <nop>
inoremap <right> <nop>

" ============================================================================
" General settings:
" ============================================================================

" stop wordwrap, except for markdown
set nowrap
autocmd FileType markdown setlocal wrap

" set spacing to 2
set tabstop=2
set shiftwidth=2
set softtabstop=2
" except in python, cause pep says 4
function! SetPythonSpacing()
  setlocal tabstop=4
  setlocal shiftwidth=4
  setlocal softtabstop=4
endfunction
autocmd FileType python call SetPythonSpacing()

" always insert spaces, but insert spaces according to the tab size
set shiftround
set expandtab

" it's sane to disable the audio bell, but the visual bell in gnome terminal is really crappy
" set visualbell

" display --instert-- in insert mode
set showmode

" display current verb in status line
set showcmd

" keep atleast this ammout of lines and columns in view around the cursor
set scrolloff=3
set sidescrolloff=5

" sane command completion settings
set wildmenu
set wildmode=list:longest
hi WildMenu ctermfg=9 ctermbg=15

" highlight current line
set cursorline
highlight clear CursorLine
highlight CursorLine ctermbg=7

" make backspace work as in other editors in insert
set backspace=indent,eol,start

" always display the statusbar
set laststatus=2

" save the undo buffer in a seperate file so that we can undo after closing
set undofile

" make ctrl vim arrow keys move in the windows
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" ============================================================================
" Search related setting:
" ============================================================================

" make searching regex behave like regular regex
nnoremap / /\v
vnoremap / /\v

" make search case insensitive when searching lowercase and case sensitive when using one or more uppercase
set ignorecase
set smartcase

" let tab be bracket matching
nnoremap <tab> %
vnoremap <tab> %


" ============================================================================
" Unsorted settings:
" ============================================================================

" source $VIMRUNTIME/delmenu.vim
" source $VIMRUNTIME/menu.vim
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
set showcmd       " display incomplete commands
set incsearch     " do incremental searching
set autowrite     " Automatically :write before running commands

" Treat <li> and <p> tags like the block tags they are
let g:html_indent_tags = 'li\|p'
syntax on

filetype indent on

" for python files, draw line at margin
autocmd FileType python setlocal colorcolumn=79 | highlight ColorColumn ctermbg=White guibg=orange

" linenumbers
set number
set numberwidth=4

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


" fix slow escape escape(ttimeoutlen) but keep the default(1 sec) slow reaction for leader (timeoutlen) 
:set timeout timeoutlen=1000 ttimeoutlen=10

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
