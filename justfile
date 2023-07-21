poetry_version := '1.3.2'

port := env_var_or_default('PORT','8004')

poetry_venv := ".poetry_venv"
poetry := poetry_venv + "/bin/poetry"
python := poetry_venv + '/bin/python'
python_version := `cat .python-version`
pre-commit := poetry_venv + '/bin/pre-commit'
uvicorn := poetry_venv + '/bin/uvicorn'
flake8 := poetry_venv + '/bin/flake8'
ruff := poetry_venv + '/bin/ruff'

# Default recipe to just --list
default:
	@just --list

# Install poetry venv
init-poetry:
	rm -rf {{poetry_venv}}
	python -m venv {{poetry_venv}}
	{{poetry_venv}}/bin/pip install poetry=={{poetry_version}}
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.path ./

# Resync
init-dev-resync:
	{{poetry}} install --all-extras -vvv

# Add package to pyproject.toml
add +ARGS:
	{{poetry}} add {{ARGS}}

# Create and initialize a local dev virtual env
init-dev: clean-all init-poetry init-dev-resync
	{{pre-commit}} install
	{{pre-commit}} install -t pre-push
	{{pre-commit}} install -t prepare-commit-msg

# Purge temporary files
clean:
	find . -name __pycache__ | xargs rm -rf
	find . -name '*,cover' -delete
	find . -name '*.swp' -delete

# Fully purge environment
clean-all: clean
	rm -rf {{poetry_venv}}

# Start the app with uvicorn in development mode
uvicorn:
	PYTHONPATH=. {{uvicorn}} lifen_app.asgi:app --host 0.0.0.0 --port {{port}} --reload

# Perform code sanity checks if needed
lint:
	{{ruff}} --ignore=E501 lifen_app
	{{flake8}} --ignore=E501 lifen_app

# Run test suite
tests:
    {{python}} -m pytest -vv tests
