# Uranus Middleware

[![Build Status](https://github.com/project-uranus/uranus-middleware/workflows/uranus/badge.svg)](https://github.com/project-uranus/uranus-middleware/actions)
[![flake8](https://img.shields.io/badge/linter-flake8-blue)](https://github.com/PyCQA/flake8)
[![yapf](https://img.shields.io/badge/formatter-yapf-blue)](https://github.com/google/yapf)

The middleware of Project Uranus based on [flask-restful](https://github.com/flask-restful/flask-restful).

## Build

The project is using [Poetry](https://github.com/sdispater/poetry) as the dependency management tool.

To install Poetry, please use the following script as recommended.

```shell
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

Then install the dependencies.

```shell
poetry install
```

## Run

Enter virtual environment then run the Flask application.

```shell
python -m uranus_middleware.app
```



## Configuration

### Visual Studio Code

In `.vscode/settings.json`:

```json
// lint
"python.linting.enabled": true,
"python.linting.lintOnSave": true,
"python.linting.pylintEnabled": false,
"python.linting.flake8Enabled": true,

// format
"python.formatting.provider": "yapf",
"[python]": {
    "editor.formatOnSave": true,
},

// testing
"python.testing.pytestEnabled": true,
```

## License

MIT
