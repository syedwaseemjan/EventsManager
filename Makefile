.PHONY: all help translate test clean update compass collect rebuild

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: test - calls the "test" django command
test:
	docker-compose exec backend pytest

coverage: # Run tests, generate coverage report, and open it
	docker-compose exec backend coverage run -m pytest
	docker-compose exec backend coverage html
	open backend/htmlcov/index.html

# target: bash
bash:
	docker-compose exec backend bash

# target: test - calls the "test" django command
shell:
	docker-compose exec backend python manage.py shell

# target: update - install (and update) pip requirements
update:
	docker-compose exec backend pip install -r requirements/local.txt

# target: collect - calls the "collectstatic" django command
collect:
	docker-compose exec backend python manage.py collectstatic --noinput

# target: collect - calls the "makemigrations" django command
migrations:
	docker-compose exec backend python manage.py makemigrations

# target: collect - calls the "migrate" django command
migrate:
	docker-compose exec backend python manage.py migrate

# target: rebuild - clean, update, collect, then rebuild all data
rebuild: clean update collect
	docker-compose exec backend python manage.py flush
	docker-compose exec backend python manage.py makemigrations
	docker-compose exec backend python manage.py migrate

loadfixtures:
	docker-compose exec backend python manage.py loaddata fixtures/users
	docker-compose exec backend python manage.py loaddata fixtures/events
	docker-compose exec backend python manage.py loaddata fixtures/participants

createsuperuser: # Create django super user
	docker-compose exec backend python manage.py createsuperuser

swagger:
	docker-compose exec backend python manage.py generate_swagger swagger.yaml -o -f yaml

# Linting #######################################################################

flake8:
	docker-compose exec backend flake8

isort:
	docker-compose exec backend isort .

black:
	docker-compose exec backend black .

lint:
	docker-compose exec backend flake8 --exit-zero
	docker-compose exec backend isort .
	docker-compose exec backend black --check .

frontendformat:
	docker-compose exec frontend npm run format

frontendlint:
	docker-compose exec frontend npm run lint --fix

