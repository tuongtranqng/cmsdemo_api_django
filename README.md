# cmsdemo_api_django
Rest APIs for CMS Demo application, implemented with Django &amp; Django Rest Framework.

## About the application
This project implements Rest APIs for a simple application used for managing classes, teachers and students in a school.

## How to run the app with Docker

## How to run the app without Docker

### Prerequisites

- Python >= 3.11

### Run the app

1. Install pipenv

```
python3 -m pip3 install pipenv
```

Or on Windows:
```
python -m pip install pipenv
```

2. Install required packages
```
pipenv sync
```

3. Activate virtual environment with pipenv
```
pipenv shell
```

4. Create .env file

    Create file .env in the project root, copy content from .env.example  
    Modify below environment variables to specify the database information:  
    
    - CMSDEMO_DB_HOST
    - CMSDEMO_DB_PORT
    - CMSDEMO_DB_NAME
    - CMSDEMO_DB_USER
    - CMSDEMO_DB_PASSWORD

    Modifying other environment variables is optional.

5. Migrate database
```
python manage.py migrate
```

6. Start the local server
```
python manage.py runserver
```
The app now should run at http://127.0.0.1:8000.

# Run unit tests
```
python manage.py test
```
