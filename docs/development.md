# Development Guide

Use python 3.10:

```
pyenv local 3.10
```

Create a virtual environment:

```
python -m venv .env
source .env/bin/activate
```

Install dependencies:

```
pip install --upgrade pip
pip install --upgrade build wheel setuptools pytest
pip install --use-pep517 ".[testing,yaml]"
```

Test:

```
pytest
```

Lint:

```
pylint munch setup.py tests
```
