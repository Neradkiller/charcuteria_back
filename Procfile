release: python ./charcuteria/manage.py makemigrations --no-input
release: python ./charcuteria/manage.py migrate --no-input

web: gunicorn charcuteria\charcuteria\wsgi --log-file -