@echo off
mkdir C:\Lab
xcopy "%~dp0Tools" C:\Lab\tools /E /I /Y
powershell -NoProfile -Command "Expand-Archive -LiteralPath '%~dp0Malware.zip' -DestinationPath 'C:\Lab\sample'"
ipconfig /all > C:\Lab\reseau-avant.txt
route print >> C:\Lab\reseau-avant.txt
powershell -NoProfile -Command "Get-NetAdapter -IncludeHidden | Format-List Name,Status,InterfaceDescription" >> C:\Lab\reseau-avant.txt
powershell -NoProfile -Command "Get-FileHash C:\Lab\sample\VIRUS\Res.exe,C:\Lab\sample\VIRUS\Env.exe | Format-List" > C:\Lab\hashes-avant.txt
start "" C:\Lab\tools\ProcessMonitor\Procmon64.exe /AcceptEula /BackingFile C:\Lab\us4.pml
