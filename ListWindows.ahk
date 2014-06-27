Loop
{
WinGet windows, List
Loop %windows%
{
	id := windows%A_Index%
	WinGetTitle wt, ahk_id %id%
	r .= wt . "`n"
}
;MsgBox %r%
run pythonw "C:/programs/popo-notify/win-notify.py" "%r%" "windows"
r = 
Sleep, 5000
}


