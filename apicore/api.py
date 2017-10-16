################################################################################
# MIT License
#
# Copyright (c) 2016 Meezio SAS <dev@meez.io>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################

from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from flask import Flask
from flask import request
from flask import jsonify
from .config import config
from .openapi import OpenAPI


class API(Flask):
    def __init__(self, import_name):
        super(API, self).__init__(import_name)
        self.prefix = ""
        self.oas = OpenAPI(config.app_name)

        # Format internal error message to JSON
        for code in default_exceptions.keys():
            # self.error_handler_spec[None][code] = self.__make_json_error
            self.register_error_handler(code, self.__make_json_error)

        # Set headers for all response
        self.after_request(self.__setHeaders)

    # Add prefix to route
    def route(self, rule, **options):
        methods = options.get("methods", ["GET"])

        def decorator(f):
            self.oas.addEndpoint(rule, methods, f.__doc__, f.__name__)
            f.__name__ = self.prefix + "_" + f.__name__
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(self.prefix + rule, endpoint, f, **options)
            return f
        return decorator

    def validate(self, func):
        def wrapper(*args, **kwargs):
            # TODO Check param, request.headers, cookies, *args, **kwargs, queryn body,... (400 et 406)
            response = self.oas.check(func.__name__, "GET")
            if response:
                return response
            else:
                return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    def fake(self, func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            # TODO si response.code  entre 200 et 300 alors oas.fake() sinon renvoi response
            return self.oas.fake(func.__name__, "GET")
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    # Return error information if debug_level = 1,
    # if 0 return HTTP code 500 and generic HTTP message
    def __make_json_error(self, ex):
        if isinstance(ex, HTTPException):
            if hasattr(ex, 'verbose') and ex.verbose:
                response = jsonify(message=ex.description)
            else:
                response = jsonify(message=str(ex))

            response.status_code = ex.code
        else:
            if config.debug:
                response = jsonify(message=str(ex))
            else:
                response = jsonify(message="Internal Server Error")
            response.status_code = 500

        return response

    # Function to be run after each request to set headers
    def __setHeaders(self, response):
        response.headers.add('Server', "{} API Server".format(config.app_name))
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers.add('Access-Control-Allow-Methods', 'DELETE, GET, HEAD, PATCH, POST, PUT')
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response

api = API(__name__)


@api.route(api.oas.endpoint)
def apispecs():
    return jsonify(api.oas.spec)
