$startup=[wmiclass]"Win32_ProcessStartup"
([wmiclass]"win32_Process").create('notepad.exe','C:\',$Startup)
