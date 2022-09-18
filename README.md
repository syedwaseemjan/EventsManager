# Assignment

## Development

Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/). Start your virtual machines with the following shell command:

`docker-compose up --build`

If all works well, you should be able to create an admin account with:

`docker-compose run backend python manage.py createsuperuser`

# Backend
Sample project to show how we can create a simple API in django.

## Instructions to install and configure prerequisites or dependencies.

At the bare minimum you'll need the following for your development environment and little knowledge of linux commands:

1. [Python 3.x](http://www.python.org)
2. [Sqlite](https://sqlite.org)

#### 3. Run the tests:

    $ make test

### Run Coverage Report

    $ make coverage

#### 4. Setup database:

    $ make migrate
    $ docker-compose run backend python manage.py createsuperuser

#### 5. Load:
    
    $ Goto http://127.0.0.1:8000/

For admin panel

    $ Goto http://127.0.0.1:8000/admin/

### Setting up commit hooks

In order to avoid submitting failing PRs, **make sure** to install pre-commit
hooks configured in this repo by running:

```
$ pip install pre-commit
$ pre-commit install
```

Now, every time you try to commit your code, `black` will automatically reformat it, `isort` will
automatically sort your imports and `flake8` will look for and report any common issues found on
the code you are trying to commit.

### Helpful Commands

There are a few commands to help you out with the task of keeping your code compliant
with python standards:

Run `isort`, `black` and `flake8` checkers:

```
$ make isort
$ make black
$ make flake8
```

