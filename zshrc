# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh
# ZSH=/usr/share/oh-my-zsh/
DEFAULT_USER="$USER"

DOTFILES=/c/WorkingFolder/GitHub/dotfiles
if [[ ! -d $DOTFILES ]]; then
  DOTFILES=$HOME/dev/dotfiles
fi

ZSH_CUSTOM=$DOTFILES/zsh_custom

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="madeso"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# gpg
export GPG_TTY=$(tty)

# make ls a* also matches American.txt
unsetopt CASE_GLOB

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"
DISABLE_UPDATE_PROMPT=true

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git
  history-substring-search
  extract
)


# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

ZSH_CACHE_DIR=$HOME/.cache/oh-my-zsh
if [[ ! -d $ZSH_CACHE_DIR ]]; then
  mkdir $ZSH_CACHE_DIR
fi

source $ZSH/oh-my-zsh.sh
export PATH=$DOTFILES/scripts:~/.local/bin/:$PATH

. $DOTFILES/external/z/z.sh

export EDITOR=vim
# export TERM=rxvt-unicode
export BROWSER=firefox

# aseprite from aur
export ASEPRITE_ACCEPT_EULA=yes

alias vi='vim'
alias open='xdg-open'

# pipe to this command to be able to paste it
alias clip='xclip -selection clipboard'

alias wb='~/dev/euphoria/tools/buildtools/Workbench/bin/Debug/net8.0/wb'

alias icat="kitty +kitten icat --align=left"

alias idot='dot -Efontsize=18 -Efontname=sans -Nfontname=sans -Tpng \
        -Gbgcolor=white -Gcolor=black -Ecolor=black -Efontcolor=black -Ncolor=black -Nfontcolor=black \
    | convert -trim -bordercolor white -border 20 -transparent white - - \
    | icat'

# history searching...
bindkey "^[[A" history-substring-search-up
bindkey "^[[B" history-substring-search-down

