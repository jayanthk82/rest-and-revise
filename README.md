Initial Instructions for developer to run in a virtual environment to run the backend. 
1: Run using python manage.py runserver in terminal 1
2: run celery -A backend worker --loglevel=info in terminal 2
3: run celery -A backend beat --loglevel=INFO  in terminal 3
4: Start docker start my-redis-mailbox
