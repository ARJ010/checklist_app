@echo off
cd /d D:\abhinav\Projects\checklist_app\cms_app
call D:\abhinav\Projects\checklist_app\venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
