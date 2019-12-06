# Uranus Middleware

[![flake8](https://img.shields.io/badge/linter-flake8-blue)](https://github.com/PyCQA/flake8)
[![yapf](https://img.shields.io/badge/formatter-yapf-blue)](https://github.com/google/yapf)

The middleware of Project Uranus based on [flask-restful](https://github.com/flask-restful/flask-restful).

## Configuration

### Visual Studio Code

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
```

## License

MIT
