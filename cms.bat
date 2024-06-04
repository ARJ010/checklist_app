@echo off
cd /d "D:\abhinav\Projects\checklist_app\cms_app"
start cmd /k python manage.py runserver
start "" http://127.0.0.1:8000/
code ..
exit
