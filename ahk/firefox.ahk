#IfWinActive ahk_class MozillaWindowClass
;MouseGetPos, [OutputVarX, OutputVarY, OutputVarWin, OutputVarControl, 1|2|3]
~WheelDown::
MouseGetPos X, Y
if ( Y < 33 )
	SendInput ^{Tab}
Return
~WheelUp::
MouseGetPos X, Y
if ( Y < 33 )
	SendInput ^+{Tab}
Return