set langmenu=en_US
let $LANG = 'en_US'
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim

if has('gui_running')
    set background=light
    colorscheme solarized
else
    colorscheme morning
endif

:set guioptions-=m  "remove menu bar
:set guioptions-=T  "remove toolbar
:set guioptions-=r  "remove right-hand scroll bar
:set guioptions-=L  "remove left-hand scroll bar

set history=50
set ruler         " show the cursor position all the time
set showcmd       " display incomplete commands
set incsearch     " do incremental searching
set laststatus=2  " Always display the status line
set autowrite     " Automatically :write before running commands

" Softtabs, 2 spaces
set tabstop=2
set shiftwidth=2
set shiftround
set expandtab

" Treat <li> and <p> tags like the block tags they are
let g:html_indent_tags = 'li\|p'
syntax on

filetype indent on

" for python files, draw line at margin
autocmd FileType python setlocal colorcolumn=79 | highlight ColorColumn guibg=orange

" linenumbers
set number
set numberwidth=4

" highlight current line
" Enable CursorLine
set cursorline

" Default Colors for CursorLine
highlight CursorLine ctermbg=Yellow guibg=#e4e4e4

" autocmd! " remove ALL autocommands

" Change Color when entering Insert Mode for all files
autocmd InsertEnter * highlight  CursorLine ctermbg=Green ctermfg=Red guibg=#ffffd7

" Revert Color to default when leaving Insert Mode for all files
autocmd InsertLeave * highlight  CursorLine ctermbg=Yellow ctermfg=None guibg=#e4e4e4

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




