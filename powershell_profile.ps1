
# https://www.howtogeek.com/50236/customizing-your-powershell-profile/

function ls_alias { wsl ls --color=auto -hF $args }
Set-Alias -Name ls -Value ls_alias -Option AllScope

# https://github.com/dahlbyk/posh-git
Import-Module posh-git

Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward

Set-PSReadlineKeyHandler -Key Tab -Function Complete
