# Assignment
A sample project showing how we can create user registration and events portal in Django 4 and Vuejs 3 where signed in users can
1. Create new events.
2. Signup for an upcoming event.
3. Withdraw from an event.

## Development

    $ git clone git@github.com:syedwaseemjan/EventsManager.git
    $ cd EventsManager

Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/). Start your containers with the following shell command:

    $ docker-compose up --build

If all works well, you should be able to load dummy data and create an admin account with:

    $ make loadfixtures (Loading fixtures to create fake data can clear existing records, therefore load them before creating any new users.)
    $ make createsuperuser

    Load http://0.0.0.0:5173/ in the browser
    Either signup or use one of the fake users
        Email: user1@example.com
        Password: test123456

### Backend

#### 1. Run the tests:

    $ make test

#### 2. Run Coverage Report

    $ make coverage

#### 3. Backend URLs
    
    APIs:  http://0.0.0.0:7000/api/v1
    Admin: http://0.0.0.0:7000/admin/

#### 4. Setting up commit hooks

In order to avoid submitting PRs having linting issues, **make sure** to install pre-commit
hooks configured in this repo by running:

    $ Install pip in your local environment (Out of docker, in your OS), if pip is not available then try pip3.
    $ pip install pre-commit
    $ pre-commit install


Now, every time you try to commit your code, `black` will automatically reformat it, `isort` will
automatically sort your imports and `flake8` will look for and report any common issues found on
the code you are trying to commit.

#### 5. Helpful Commands

There are a few commands to help you out with the daily tasks:

Run `isort`, `black` and `flake8` checkers:


    $ make isort
    $ make black
    $ make flake8


To create new migration and apply them:

    $ make migrations
    $ make migrate

To flush DB, reapply all migrations, reload dummy data and re-create superuser:

    $ make rebuild
    $ make loadfixtures
    $ make createsuperuser

#### 6. Building Swagger/OpenAPI 2.0 schema file

To generate an OpenAPI 2.0 schema based API doc, run the following command:

    $ make swagger

Above command needs to be run whenever new API endpoints are added. If auto generated schema needs manual changes then use [swagger_auto_schema](https://drf-yasg.readthedocs.io/en/stable/custom_spec.html#the-swagger-auto-schema-decorator) decorator.

To provide response examples, create an `api_examples` directory in the respective app and then set the path of JSON response in `responses>examples` of `swagger_auto_schema`:

```python
    test_view_schema = swagger_auto_schema(
        operation_description='Test view.',
        request_body=BlaSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                'Test resource created successfully.',
                RateTableSerializer,
                examples={
                    'application/json': 'apps/events/api_examples/test.json',
                }
            )
        }
    )
```

You can view the schema using Swagger UI by visiting [http://0.0.0.0:7000/swagger/](http://0.0.0.0:7000/swagger/) in browser.

drf-yasg [documentation](https://drf-yasg.readthedocs.io/en/stable/).

#### 7. API documentation:

- [OpenAPI 2.0 based documentation](http://0.0.0.0:7000/swagger/).

### Frontend

#### 1. Format and Lint the js and vue code

    $ make frontendformat
    $ make frontendlint

## Features

- Backend
  - [Python 3.9](https://www.python.org/)
  - [Django 4.0](https://www.djangoproject.com/)
  - [Django REST framework](https://www.django-rest-framework.org/)
  - [Dj-Rest-Auth](https://dj-rest-auth.readthedocs.io/)
- Frontend
  - [ES6](http://es6-features.org/#Constants)
  - [Vue.js 3.0](https://vuejs.org/)
  - [Quasar Framework](https://quasar.dev/)
  - [Pinia](https://pinia.vuejs.org/)
