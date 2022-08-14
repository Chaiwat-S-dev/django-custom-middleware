# Project Title

**This is project web API base on python django REST frameworks**

## Database
 - Postgresql

## Database GUI
 - Pgadmin

## Cache
 - Redis

## Cache GUI
 - Redis Desktop Manager

## Enviroment
 - Python 3.8.10
 - Pip

## Suggestion
 - Virtual enviroment can install follow **requirements.txt**
 - Config connetion to postgres database in setting.py
 - Config connetion to redis in setting.py

### Run virtual enviroment
 ```
 source django_custom_middleware/virtualenv/bin/activate
 ```
### Migrate model
 ```
 python3 manage.py migrate
 ``` 
 ### Seed data to DB
 ```
 python3 manage.py seed
 ``` 
### Run app
 ```
 python3 manage.py runserver
 ```