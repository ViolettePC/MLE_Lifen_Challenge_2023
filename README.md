# Minimal MLE challenge micro-service

## How to set-up the environment ?

> Prerequisites
>
> - pyenv
> - Python 3.11
> - Docker & Docker Compose

### Init the development environment via:

```bash
just init-dev
```

### Run the app via:

```bash
just uvicorn
```

## From docker

A docker-compose.yml file is available to easier the docker build and run steps. The docker can be built and run via the following command:

```bash
docker-compose up
```

### Use the terminal in Docker

```bash
docker-compose exec <service-name> /bin/bash
```

Then you can run any script you want in your Docker.

## Test suite

A test suit is available and can be run from the justfile

```bash
just test
```
