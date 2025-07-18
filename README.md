# API Core

Core lib for building REST API in Python 3.

Documentation available at [http://apicore.readthedocs.io/en/latest/](http://apicore.readthedocs.io/en/latest/)

## Features

## Déploiement d'une nouvelle version sur Pypi

```bash
python3 -m venv venv
source venv/bin/activate
pip install build twine
```

```bash
rm dist/*
# Changer le numéro de version
vi pyproject.toml 
source venv/bin/activate
python -m build
twine upload dist/*
git add -A .
git commit -m "Release x.y.z"
git push --tags
```
