#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

SetTitleMatchMode 2

; -------------------------------------------------------------------------------------------------------------------
; media controls
; -------------------------------------------------------------------------------------------------------------------

; used - 1 when button has done its job and shouldnt play/pause when released
used = 1
Return

; some callbacks are based on the script frome here https://autohotkey.com/board/topic/36239-spotify-global-hotkeys/
; play/pause doesnt seem to work so the global media button is used instead

SC056::
used = 0
Return

SC056 UP::
if(used = 0)
{
  Send {Media_Play_Pause}
}
Return

SC056 & Space::
DetectHiddenWindows, On 
ControlSend, ahk_parent, ^S, ahk_class SpotifyMainWindow 
DetectHiddenWindows, Off
used = 1
Return

SC056 & Right::
;Send {Media_Next}
used = 1
DetectHiddenWindows, On 
ControlSend, ahk_parent, ^{Right}, ahk_class SpotifyMainWindow 
DetectHiddenWindows, Off 
Return

SC056 & Left::
;Send {Media_Prev}
used = 1
DetectHiddenWindows, On 
ControlSend, ahk_parent, ^{Left}, ahk_class SpotifyMainWindow 
DetectHiddenWindows, Off 
Return

SC056 & Up::
Send {Volume_Up}
used = 1
Return

SC056 & Down::
Send {Volume_Down}
used = 1
Return

SC056 & C::
used = 1
DetectHiddenWindows, On
WinGetTitle, now_playing, ahk_class SpotifyMainWindow
DetectHiddenWindows, Off
clipboard = %now_playing%
Return

; -------------------------------------------------------------------------------------------------------------------
; swedish characters
; -------------------------------------------------------------------------------------------------------------------

RAlt::Return

>!Q::
Send ä
Return

>!+Q::
Send Ä
Return

>!W::
Send å
Return

>!+W::
Send Å
Return

>!P::
Send ö
Return

>!+P::
Send Ö
Return

; -------------------
; capslock to escape
; -------------------

Capslock::Esc

