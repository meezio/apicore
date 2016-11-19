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

import json
from flask import request
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from urllib.request import urlopen
from .exceptions import Http401Exception, Http403Exception
from .config import config


def Authorization():
    # Authorization required
    if "Authorization" not in request.headers:
        raise Http401Exception("No Authorization header present")

    # Get JWT from HTTP headers
    auth = request.headers.get("Authorization").split()
    if len(auth) is not 2 and auth[0] is not "Bearer":
        raise Http403Exception("Malformed Authorization HTTP Header : format MUST match Bearer TOKEN.")

    # Find the token issuer
    try:
        tmp = jwt.get_unverified_claims(auth[1])
        issuer = tmp.get('iss')
    except JWTError as ex:
        raise Http403Exception(str(ex))
    if not issuer:
        raise Http403Exception("'iss' claim missing in JWT.")

    # If whitelist is empty every issuers are allowed except those from blacklist
    if config.issWhitelist:
        if issuer not in config.issWhitelist:
            raise Http403Exception("Issuer '{}' not in Whitelist.".format(issuer))
    if config.issBlacklist:
        if issuer in config.issBlacklist:
            raise Http403Exception("Issuer '{}' is blacklisted.".format(issuer))

    # Get the issuer's keys
    # TODO Use a cache (redis) => parcourir toute les clée et voir exp le plus petit pour fixer timeout du cache
    oidcConf = getJSON("{}/.well-known/openid-configuration".format(issuer))
    keys = getJSON(oidcConf.get("jwks_uri")).get("keys")

    try:
        userProfile = jwt.decode(auth[1], keys, options={"verify_aud": False, "verify_iss": False, "verify_sub": False, "verify_exp": config.tokenExpire})
        return userProfile
    except ExpiredSignatureError as ex:
        raise Http403Exception(str(ex), True)
    except JWTError as ex:
        raise Http403Exception(str(ex))


def getJSON(url):
    data = urlopen(url).read().decode("utf-8")
    return json.loads(data)
