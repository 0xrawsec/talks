Import-Module 'C:\Users\Gen Eric\Desktop\Invoke-ReflectivePEInjection.ps1'
$PEBytes = [IO.File]::ReadAllBytes('C:\Users\Gen Eric\Desktop\hello-world.dll')
Invoke-ReflectivePEInjection -PEBytes $PEBytes -ProcName explorer