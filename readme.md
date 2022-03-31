
# Project Title

> A Blog Application API in `Django Rest Framework(DRF)` for those who wants to learn DRF in depth.

## Project Setup


Initial requirements:
```
    python
    MySQL (PREFERRED BUT NOT REQUIRED)
```

To Setup this project at your local pls follow these steps:

1. Clone the repo at your local.

    `git clone -b master GIT_REPO_URL`

2. Now, create and activate virtualenvironment.

    `virtualenv YOUR_VENV_NAME`

    Linux: `source YOUR_VENV_NAME/bin/activate`

    Windows: `PATH_TO_YOUR_VENV\Scripts\activate`

3. Change directory(cd) where `requirements.txt` file is present and run:

    `pip install -r requirements.txt`

4. `[skip this step if you don't want to use MySQL]` Now, create a database in MySQL and a user and grant permissions to newly created user on database.

    MySQL create db and user:
    http://localhost:8000/api/
    `sudo mysql -u'root'`

    Create DB: `CREATE DATABASE new_database;`

    List all DB: `SHOW DATABASES;`

    Create User: `CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';`

    GRANT ALL PERMISSIONS on the database:

    `GRANT ALL PRIVILEGES ON new_database.* TO 'username'@'localhost' WITH GRANT OPTION;`

    Then run: `FLUSH PRIVILEGES;` to make sure all changes have been made.


5. If you have skipped 4th step then replace this with `DATABASE` in `settings.py` file:

    BEFORE:
    ```
    DATABASES = {
        'default': {
            'ENGINE': ENV.get('MySQL_ENGINE'),
            'NAME': ENV.get('MySQL_DB_NAME'),
            'USER': ENV.get('MySQL_USER'),
            'PASSWORD': ENV.get('MySQL_PASSWORD'),
            'HOST': ENV.get('HOST', 'localhost'),
            'PORT': ENV.get('PORT', '3306')
        }
    }
    ```
    NOW:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```


6. Now, rename `.env.example` to `.env` and replace the variable's value according to yours.

7. change directory(cd) where `manage.py` file is present and run these commands:

    `python manage.py makemigrations`

    `python manage.py migrate`

8. To django runserver:
    `python manage.py runserver`


9. now go to [http://localhost:8000/api/](http://localhost:8000/api/) or [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

10. To list all the paths/endpoints available:

    go to [http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/)

    or in another terminal run `python manage.py show_urls`


## Authors

- [@Sheraram Prajapat](https://github.com/SheraramPrajapat1998)

<div>
<a href="https://www.linkedin.com/in/sheraramprajapat1998" target="_blank">
<img src=https://img.shields.io/badge/linkedin-%231E77B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white alt=linkedin style="margin-bottom: 5px;" />
</a>
</div>



## Documentation

[Documentation](#project-setup)


## Environment Variables

To run this project, you will need to rename `.env.example` to `.env` and make necessary changes
