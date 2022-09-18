FROM python:3.9

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# python dependencies

COPY requirements /requirements
RUN pip install --upgrade pip && pip install -r ./requirements/local.txt

# upload scripts
COPY ./scripts/start.sh /

WORKDIR /app
