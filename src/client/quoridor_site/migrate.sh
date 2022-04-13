yarn
python3 manage.py compress
python3 manage.py makemigrations quoridor_site_backend admin
python3 manage.py migrate 
touch ./quoridor_site_backend/urls.py