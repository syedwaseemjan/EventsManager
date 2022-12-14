#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

pip install -r ./requirements/local.txt

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0
python manage.py runserver 0.0.0.0:7000
