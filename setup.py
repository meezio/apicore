"""
apicore
=======

Set of core libraries usefull for building REST API and Microservices based on Flask.

The code is open source, release under MIT and written in Python 3.

.. code:: bash

    pip install apicore


Features
--------

* Cross-origin resource sharing (CORS) ready
* Data caching with redis server or in-memory
* Configuration file loader
* A simple Logger
* Raise exception conform to HTTP status codes
* Authorization using JSON Web Token(JWT) issued from an OpenID Connect provider.

Links
-----

* `Documentation <http://apicore.readthedocs.io/en/latest/>`_
* `Source code <https://github.com/meezio/apicore>`_
* `Company <https://meez.io>`_
"""

from setuptools import setup, find_packages

setup(
    name='apicore',
    version='1.2.0',
    # packages=['apicore'],
    packages=find_packages(),
    author="Meezio SAS",
    author_email="dev@meez.io",
    description="Core lib for REST API",
    long_description=__doc__,
    include_package_data=True,
    url='https://github.com/meezio/apicore',
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        "Topic :: Software Development :: Libraries"
    ],
    license="MIT",
    install_requires=[
        'termcolor',
        'Flask',
        'PyYAML',
        'redis',
        'pystache',
        'jsonschema'
    ]
)
