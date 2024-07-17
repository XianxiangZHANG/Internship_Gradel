# Internship_GRADEL
## Database of Gradel
 Auther: Xianxiang ZHANG

Created a database by Django.

### Run the project:
```
python manage.py runserver
```

### Run the Celery:
```
celery -A database worker --loglevel=info
celery -A database beat --loglevel=info
```