#!/usr/bin/env python

from apicore import api, Logger, config, Http409Exception, Authorization

config.load('config.yaml')
Logger.info("{} started".format(config.server_name))
api.prefix = "/api"


@api.route('/', methods=['GET', 'PUT', 'POST', 'DELETE', 'PATCH'])
def hello():
    return "API v0.1"


@api.route('/error/')
def error():
    raise Http409Exception()


@api.route('/jwt/')
def jwt():
    userProfile = Authorization()
    print(userProfile)
    return "JWT Valid!"


if __name__ == "__main__":
    api.debug = config.debug
    api.run()
