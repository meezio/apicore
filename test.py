#!/usr/bin/env python

from apicore import api, Logger, config, Http402Exception, Lang
from tests import oascheck

Logger.info("Starting {} API Server...".format(config.app_name))


@api.route('/error/', methods=['GET', 'PUT', 'POST', 'DELETE', 'PATCH'])
def error():
    print(Lang.best_match(['it', 'en', 'fr']))
    raise Http402Exception()


if __name__ == "__main__":
    api.debug = config.debug
    api.run()
