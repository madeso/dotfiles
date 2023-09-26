
# https://www.howtogeek.com/50236/customizing-your-powershell-profile/


# make ls behave like ls on linux...


function ls_alias { Get-ChildItem $args -Exclude .*  | Format-Wide Name -AutoSize }
Set-Alias -Name ls -Value ls_alias -Option AllScope

# which
New-Alias which get-command

# add git-status in prompt: https://github.com/dahlbyk/posh-git
Import-Module posh-git

# make up/down arrows sane
Set-PSReadlineOption -HistorySearchCursorMovesToEnd
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward

# make tab complition more sane
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete


# disable prediction
# https://devblogs.microsoft.com/powershell/announcing-psreadline-2-1-with-predictive-intellisense/
Set-PSReadLineOption -PredictionSource None
