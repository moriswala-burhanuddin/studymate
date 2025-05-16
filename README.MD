Before deploying STUDYMATE, follow these  steps to ensure a smooth and secure deployment:

✅ 1. Update Production Settings (studymates/settings.py)
Set DEBUG = False
in studymates\studymates\settings.py

Set ALLOWED_HOSTS
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'server-ip']

Set a Secure SECRET_KEY
Don’t hardcode in production; use environment variable instead.

📂 2. Static & Media File Configuration -Already collected static files — no need to run collectstatic.

🌐 3. Serve Static & Media in Production
If using Nginx, add this inside your Nginx config block:

nginx
Copy
Edit
location /static/ {
    alias /full/path/to/studymates/staticfiles/static/;
}

location /media/ {
    alias /full/path/to/studymates/media/;
}
📝 Replace /full/path/to/ with the absolute server path.

python version = Python 3.13.0


to run project 
python manage.py runserver 
Install requirements.txt 