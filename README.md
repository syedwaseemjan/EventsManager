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

### Building Swagger/OpenAPI 2.0 schema file

To generate a swagger schema file run the following command:

    $ python manage.py generate_swagger swagger.yaml -o -f yaml

Whenever new API endpoints are created, running `generate_swagger` will create the schema for it. However, if auto generated schema needs manual changes then use [swagger_auto_schema](https://drf-yasg.readthedocs.io/en/stable/custom_spec.html#the-swagger-auto-schema-decorator) decorator.

To provide response examples, create an `api_examples` directory in the respective app and then set the path of JSON response in `responses>examples` of `swagger_auto_schema`:

```python
    bla_bla_view_schema = swagger_auto_schema(
        operation_description='Creates bla bla.',
        request_body=BlaSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                'BlaBla created successfully.',
                RateTableSerializer,
                examples={
                    'application/json': 'apps/events/api_examples/bla.json',
                }
            )
        }
    )
```

You can view the schema using Swagger UI by visiting [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) in browser.

I am using [drf-yasg](https://github.com/axnsan12/drf-yasg) package for generation of schema and it's documentation can be found [here](https://drf-yasg.readthedocs.io/en/stable/).

### The API

You can find the API documentation in:

- [This project's swagger file](http://127.0.0.1:8000/swagger/).


