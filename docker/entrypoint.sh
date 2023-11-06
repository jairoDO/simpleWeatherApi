cd weather_api
./manage.py makemigrations
./manage.py migrate
./manage.py runserver 0:80
./manage.py generate_db_entries --count 20