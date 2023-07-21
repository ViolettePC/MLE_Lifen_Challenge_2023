ARG APP_NAME=lifen_app
ARG APP_PATH=/opt/$APP_NAME
ARG POETRY_HOME=/opt/poetry

#
# Stage: Build
#
FROM python:3.11.0-slim AS builder

ARG APP_PATH
ARG APP_NAME
ARG POETRY_HOME

WORKDIR $APP_PATH
COPY ./poetry.lock ./pyproject.toml ./
COPY ./$APP_NAME ./$APP_NAME

RUN apt-get update -y && apt-get upgrade -y && apt-get install curl -y
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN poetry export -f requirements.txt >> requirements.txt

#
# Stage: development
#
FROM builder as development

ARG APP_PATH

WORKDIR $APP_PATH

RUN poetry install

EXPOSE 80

CMD ["uvicorn", "lifen_app.asgi:app", "--host", "0.0.0.0", "--port", "80"]
