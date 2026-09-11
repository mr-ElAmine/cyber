@echo off
cd /d C:\Lab\sample\VIRUS
echo Debut de l'essai : %date% %time% > C:\Lab\essai.txt
start "" Res.exe
timeout /t 15 /nobreak
echo Lancement Env : %date% %time% >> C:\Lab\essai.txt
start "" Env.exe
timeout /t 60 /nobreak
tasklist /FI "IMAGENAME eq Res.exe" >> C:\Lab\essai.txt
tasklist /FI "IMAGENAME eq Env.exe" >> C:\Lab\essai.txt
netstat -ano > C:\Lab\reseau-apres.txt
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run >> C:\Lab\essai.txt
dir C:\WindSyst >> C:\Lab\essai.txt
taskkill /IM Res.exe /F >> C:\Lab\essai.txt 2>&1
taskkill /IM Env.exe /F >> C:\Lab\essai.txt 2>&1
echo Fin de l'essai : %date% %time% >> C:\Lab\essai.txt
echo Essai termine. Arreter et fermer Process Monitor pour conserver la trace.
pause
