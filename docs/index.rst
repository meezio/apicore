Welcome to apicore's documentation!
===================================

Set of core libraries usefull for building REST API and Microservices based on Flask.

The code is open source, release under MIT and written in Python 3.

.. code:: bash

    pip install git+https://github.com/meezio/apicore.git

Features
--------

* Cross-origin resource sharing (CORS) ready
* Data caching with redis server or direct in memory
* Configuration file loader
* A simple Logger
* Raise exception conform to HTTP status codes
* Authorization using JSON Web Token(JWT) issued from an OpenID Connect provider.

Sample
------

.. code:: python

    #!/usr/bin/env python

    from apicore import api, Logger, config, Http409Exception, Authorization

    config.load('config.yaml')
    Logger.info("{} Starting".format(config.server_name))
    api.prefix = "/api"


    @api.route('/')
    def hello():
        return "API v0.1"


    @api.route('/error/')
    def error():
        raise Http409Exception()


    @api.route('/jwt/')
    def jwt():
        userProfile = Authorization()
        print(userProfile);
        return "JWT Valid!"


    if __name__ == "__main__":
        api.debug = config.debug
        api.run()


Configuration
-------------

Configuration is set in a YAML file @see apicore.config

+--------------+---------------+------------------------------------------------------------------------------------------------+
| Name         | Default value | Description                                                                                    |
+==============+===============+================================================================================================+
| server_name  | 'API server'  | Service name.                                                                                  |
+--------------+---------------+------------------------------------------------------------------------------------------------+
| debug        | True          | Active debug mode.                                                                             |
+--------------+---------------+------------------------------------------------------------------------------------------------+
| issWhitelist | None          | Whitelist for OIDC issuers. If not set, every issuers are allowed except ones from blacklist.  |
+--------------+---------------+------------------------------------------------------------------------------------------------+
| issBlacklist | None          | Blacklist for OIDC issuers. synaxte : same as 'iss' claim in the JWT.                                |
+--------------+---------------+------------------------------------------------------------------------------------------------+
| tokenExpire  | True          | Check 'exp' claim in JWT to validate token.                                                          |
+--------------+---------------+------------------------------------------------------------------------------------------------+
| redis        | None          | Redis server used for caching data : redis://:password@localhost:6379/0. If not set use memory.|
+--------------+---------------+------------------------------------------------------------------------------------------------+

APIs
----

.. toctree::
   :maxdepth: 2

   api/api
   api/authorization
   api/cache
   api/config
   api/exceptions
   api/logger

TODO
----

* i18n HTTP messages : default in english, build app can translate to other language => document messge variable here.
* Command line argument & env variable to overide config file
