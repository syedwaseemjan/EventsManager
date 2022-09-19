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
	docker-compose run backend pytest -n auto $(PYTEST_ARGS)

coverage: # Run tests, generate coverage report, and open it
	docker-compose run backend coverage run -m pytest -n auto
	docker-compose run backend coverage html
	open htmlcov/index.html

# target: bash
bash:
	docker-compose exec backend bash

# target: test - calls the "test" django command
shell:
	docker-compose run backend python manage.py shell

# target: update - install (and update) pip requirements
update:
	docker-compose run backend pip install -r requirements/local.txt

# target: collect - calls the "collectstatic" django command
collect:
	docker-compose run backend python manage.py collectstatic --noinput

# target: collect - calls the "makemigrations" django command
migrations:
	docker-compose run backend python manage.py makemigrations

# target: collect - calls the "migrate" django command
migrate:
	docker-compose run backend python manage.py migrate

# target: rebuild - clean, update, collect, then rebuild all data
rebuild: clean update collect
	docker-compose run backend python manage.py reset_db --noinput
	docker-compose run backend python manage.py makemigrations
	docker-compose run backend python manage.py migrate

# Linting #######################################################################

flake8: # Run flake8
	docker-compose run backend flake8

isort: # Run isort recursively and fix the imports order
	docker-compose run backend isort .

isort.checkonly: # Run isort recursively but only check for improper imports order
	docker-compose run backend isort . --check-only

lint: # Run the black code format checker and flake8 checkers (pep-8, pyflakes, isort, mccabe)
	docker-compose run backend flake8 --exit-zero
	docker-compose run backend black --check .

black: # Reformat code using black
	docker-compose run backend black .

format: # Reformat code using black (for code style) and isort (for imports order)
	docker-compose run backend black .
	@$(MAKE) -f $(THIS_FILE) isort
