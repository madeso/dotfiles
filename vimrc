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

" set spacing to 4
set tabstop=4
set shiftwidth=4
set softtabstop=4

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
highlight CursorLine ctermbg=5

" cursor style
" Set IBeam shape in insert mode, underline shape in replace mode and block shape in normal mode. 
" https://vim.fandom.com/wiki/Change_cursor_shape_in_different_modes#For_VTE_compatible_terminals_.28urxvt.2C_st.2C_xterm.2C_gnome-terminal_3.x.2C_Konsole_KDE5_and_others.29_and_wsltty
let &t_SI = "\<Esc>[6 q"
let &t_SR = "\<Esc>[4 q"
let &t_EI = "\<Esc>[6 q"

" make backspace work as in other editors in insert
set backspace=indent,eol,start

" always display the statusbar
set laststatus=2

" save the undo buffer in a seperate file so that we can undo after closing
set undofile

" reload vimrc when saved
au BufWritePost .vimrc so ~/.vimrc


" ============================================================================
" Search related setting:
" ============================================================================

" make searching regex behave like regular regex
" nnoremap / /\v
" vnoremap / /\v

" make search case insensitive when searching lowercase and case sensitive when using one or more uppercase
set ignorecase
set smartcase



" ============================================================================
" Unsorted settings:
" ============================================================================

" source $VIMRUNTIME/delmenu.vim
" source $VIMRUNTIME/menu.vim

" syntastic
execute pathogen#infect()

" make find command look in current folder too
set path+=**

function! SyntaxItem()
  return synIDattr(synID(line("."),col("."),1),"name")
endfunction

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
set statusline+=\ 
set statusline+=%{SyntaxItem()}

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
let g:syntastic_auto_loc_list = 0
let g:syntastic_check_on_open = 0
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
autocmd FileType python setlocal colorcolumn=79 | highlight ColorColumn ctermbg=14 guibg=orange
autocmd FileType cpp setlocal colorcolumn=79 | highlight ColorColumn ctermbg=14 guibg=orange

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


:au FocusLost * :set nornu
:au FocusGained * :set rnu

autocmd InsertEnter * :set nornu
autocmd InsertLeave * :set rnu


" fix slow escape escape(ttimeoutlen) but keep the default(1 sec) slow reaction for leader (timeoutlen) 
:set timeout timeoutlen=1000 ttimeoutlen=10



" ============================================================================
" Keyboard shortcuts (common)
" ============================================================================

" make enter in normal enter a new line
nmap <CR> o<Esc>


" let tab be bracket matching
nnoremap <tab> %
vnoremap <tab> %


" ============================================================================
" Keyboard shortuts (leader)
" ============================================================================

" https://stackoverflow.com/a/11993928/180307
nnoremap <leader>c "_c
nnoremap <leader>d "_d
xnoremap <leader>d "_d
xnoremap <leader>p "_dP

" use leader w to save all files (mostly for testing leader action currently)
nnoremap <leader>w :wa<CR>

" open vimrc in a vertical split
nnoremap <leader>ev <C-w><C-v><C-l>:e $MYVIMRC<cr>

" edit vimrc quickly
map <leader>v :sp ~/.vimrc<cr>


" ============================================================================
" Keyboard shortcuts (Ctrl)
" ============================================================================

" nnoremap <C-n> :call NumberToggle()<cr>

" ctrl n+p to switch buffers
" nnoremap <C-n> :bnext<CR>
" nnoremap <C-p> :bprevious<CR>

" hrmm... does tab and shift tab work?
nnoremap <C-b> :bnext!<CR>
nnoremap <C-S-b> :bprev!<CR><Paste>

" make ctrl-y and ctrl-p copy and paste from system clipboard
nnoremap <C-y> "+y
nnoremap <C-p> "+p

" move lines or blocks up/down with alt+movment
" not any more, I should learn to yank and paste intead...
" nnoremap <C-j> :m .+1<CR>==
" nnoremap <C-k> :m .-2<CR>==
" inoremap <C-j> <Esc>:m .+1<CR>==gi
" inoremap <C-k> <Esc>:m .-2<CR>==gi
" vnoremap <C-j> :m '>+1<CR>gv=gv
" vnoremap <C-k> :m '<-2<CR>gv=gv

" make ctrl vim arrow keys move in the windows
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" ============================================================================
" Commands
" ============================================================================

" fomat json with python
com! FormatJson %!python -m json.tool

" transform windows line endings to linux (probably)
com! Ln %s/^M/\r/g

hi Visual ctermbg=14

hi jsonNoQuotesError ctermfg=10 ctermbg=5
hi jsonCommentError ctermfg=2 ctermbg=5

hi vimBracket ctermfg=3
hi vimNotation ctermfg=1
hi vimMapModkey ctermfg=0
hi vimOption ctermfg=1
hi vimEnvvar ctermfg=1

hi pythonEscape ctermfg=1

hi shOption ctermfg=1
hi shCmdSubRegion ctermfg=0
hi shCommandSub ctermfg=2
hi shParen ctermfg=3

hi htmlH3 ctermfg=1
hi htmlLink ctermfg=2

hi PreProc ctermfg=1
hi Delimiter ctermfg=2

hi htmlSpecialChar ctermfg=1
hi htmlTitle ctermfg=1
hi javaScript ctermfg=1
hi cssAttrComma ctermfg=1
hi cssUnicodeEscape ctermfg=1

hi gitcommitBranch ctermfg=1
hi gitcommitHeader ctermfg=1

hi pythonInclude ctermfg=1

hi markdownHeadingDelimiter ctermfg=2
hi markdownH1 ctermfg=2
hi markdownH2 ctermfg=1
hi markdownLinkText ctermfg=4
hi markdownCodeDelimiter ctermfg=1
hi markdownListMarker ctermfg=1

hi cInclude ctermfg=1
hi cSpecialCharacter ctermfg=1
hi cSpecial ctermfg=1
hi cFormat ctermfg=1
hi cDefine ctermfg=2
hi cPreCondit ctermfg=2

hi cppRawString ctermfg=1


hi yamlKeyValueDelimiter ctermfg=2
hi yamlFlowIndicator ctermfg=1

hi dtGroup ctermfg=1

hi jsonBraces ctermfg=2

" editorconfig
hi dosiniHeader ctermfg=1

