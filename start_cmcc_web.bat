@echo off
chcp 65001 >nul
cd /d "C:\Users\Smallsun\Documents\Daily Work\cmcc-daily"
"C:\Users\Smallsun\AppData\Local\Programs\Python\Python312\python.exe" -m cmcc_app serve >> web.log 2>&1
