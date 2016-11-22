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

import yaml
from .logger import Logger
from .exceptions import Http500Exception


class Config:
    """ Manage configuration values.
    To use by importing the instance :

    exemple:
        .. code::

            from apicore import config

            print(config.server_name)


    """
    def __init__(self):
        self.data = dict()
        self.__setDefault()

    def load(self, confFile='config.yaml'):
        """ Load config file from filesystem.

        :param str string: Path to config file.
        """
        try:
            with open(confFile) as f:
                data = yaml.load(f)
                if data:
                    self.data.update(data)
        except FileNotFoundError:
                Logger.error("Configuration file not found")

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise Http500Exception("Config value '{}' does not exist.".format(name))

    def __setDefault(self):
        # Service name
        self.data['server_name'] = "API server"
        # Active debug
        self.data['debug'] = True
        # Accept all JWT from issuers from this list
        self.data['issWhitelist'] = None
        # Reject all JWT from issuers from this list
        self.data['issBlacklist'] = None
        # Validate token against Expire date/time
        self.data['tokenExpire'] = True
        # redis://:password@localhost:6379/10
        self.data['redis'] = None

config = Config()
