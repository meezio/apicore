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

import smtplib
from email.parser import Parser
import pystache
from .config import config


class Mail:
    """ Cache for the application.
    To use by importing the instance :

    exemple:
        .. code::

            from apicore import Mail

            mail = Mail("noreply@domain.tld", "john@doe.tld")
            mail.setSubject("TEST")
            mail.setContent("Hello", data)
            mail.send()


    .. note::

        If ``redis`` URI is configured the cache is store in redis server, otherwise it is cache in memory.

    """
    def __init__(self, exp, rcpt):
        self._host = config.smtp_host
        self._exp = exp
        self._rcpt = rcpt

    def setContent(self, messagefile, data):
        with open(messagefile) as f:
            template = f.read()

        self._message = pystache.render(template, data)

    def send(self):
        s = smtplib.SMTP(self._host)
        s.set_debuglevel(config.debug)
        s.sendmail(self._exp, self._rcpt, self._message.encode("utf8"))
        s.quit()
