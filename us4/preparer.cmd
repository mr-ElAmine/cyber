@echo off
rem Preparation dans la VM Windows isolee.

rem Copier les outils et extraire le lot a examiner.
mkdir C:\Lab
xcopy "%~dp0Tools" C:\Lab\tools /E /I /Y
powershell -NoProfile -Command "Expand-Archive -LiteralPath '%~dp0Malware.zip' -DestinationPath 'C:\Lab\sample'"

rem Enregistrer la configuration reseau avant l'essai.
ipconfig /all > C:\Lab\reseau-avant.txt
route print >> C:\Lab\reseau-avant.txt
powershell -NoProfile -Command "Get-NetAdapter -IncludeHidden | Format-List Name,Status,InterfaceDescription" >> C:\Lab\reseau-avant.txt

rem Identifier les deux executables par leurs empreintes.
powershell -NoProfile -Command "Get-FileHash C:\Lab\sample\VIRUS\Res.exe,C:\Lab\sample\VIRUS\Env.exe | Format-List" > C:\Lab\hashes-avant.txt

rem Ouvrir Process Monitor avant tout lancement du malware.
start "" C:\Lab\tools\ProcessMonitor\Procmon64.exe /AcceptEula /BackingFile C:\Lab\us4.pml
