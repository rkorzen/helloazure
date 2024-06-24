python manage.py migrate
gunicorn hello_azure.wsgi:application --bind 0.0.0.0:8000