#!/usr/bin/env python

from apicore import API, Logger, config, Http409Exception

config.load('config.yaml')
api = API(__name__)
Logger.info("Démarrage de {}".format(config.server_name))
api.prefix = "api"


@api.route('/')
def hello():
    return "API v0.1"


@api.route('/error/')
def error():
    raise Http409Exception()


if __name__ == "__main__":
    api.debug = config.debug
    api.run()
