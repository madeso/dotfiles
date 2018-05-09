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

SC056::
used = 0
Return

SC056 UP::
if(used = 0)
{
  Send {Media_Play_Pause}
}
Return

SC056 & Right::
Send {Media_Next}
used = 1
Return

SC056 & Left::
Send {Media_Prev}
used = 1
Return

SC056 & Up::
Send {Volume_Up}
used = 1
Return

SC056 & Down::
Send {Volume_Down}
used = 1
Return

; -------------------
; capslock to escape
; -------------------

Capslock::Esc

