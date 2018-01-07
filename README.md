# API Core

Core lib for building REST API in Python 3.

Documentation available at http://apicore.readthedocs.io/en/latest/

## Features

* Cross-origin resource sharing (CORS) ready
* Data caching with redis server or direct in memory
* Configuration file loader
* A simple Logger
* Raise exception conform to HTTP status codes
* Authorization using JSON Web Token(JWT) issued from an OpenID Connect provider
* OpenAPI 3.0 specification embedded with Swagger UI

## Release cheat sheet

* Update version in ``setup.py``.
* Update doc
```
cd docs
make html
cd ..
```
* git
```
git commit -m ""
git checkout master
git merge develop
git tag x.y.z
git push --tags
git push
```
* PyPI
```
python setup.py test
python setup.py sdist
twine upload dist/*
```
* Docker
```
cd docker
docker build --build-arg VERSION=x.y.z -t meezio/apicore .
docker tag meezio/apicore meezio/apicore:x.y.z
docker tag meezio/apicore meezio/apicore:x.y
docker tag meezio/apicore meezio/apicore:x
docker push meezio/apicore
```
