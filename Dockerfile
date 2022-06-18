###############################################
# Base Image
###############################################
FROM python:3.10-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    APP_ENV=Production

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
###############################################
# Builder Image
###############################################
FROM python-base as builder-base
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip3 install poetry 

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install 

###############################################
# Production Image
###############################################
FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /APP

# Clone app and npm install on server
ENV URL_TO_APPLICATION_GITHUB="https://github.com/lapig-ufg/GEEController-server.git"
ENV BRANCH="main"

RUN apt-get update && apt-get install -y git && mkdir -p /APP && mkdir -p /data && \
    cd /APP && git clone -b ${BRANCH} ${URL_TO_APPLICATION_GITHUB} && \
    pip install gunicorn[gevent] && \
    rm -rf /var/lib/apt/lists/*

CMD sh -c "cd /APP/GEEController-server && gunicorn --worker-class gevent --workers 4 --bind 0.0.0.0:5000 ServeStatus.wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info && tail -f /dev/null"
