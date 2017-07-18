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
import datetime
import time
from flask import request
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from urllib.request import urlopen
from .logger import Logger
from .exceptions import Http401Exception, Http403Exception
from .config import config
from .cache import cache


def Authorization():
    """ Check that JSON Web Token (JWT) passed through ``Authorization`` header or through  query parameter 'token' is valid.
    The JWT MUST be provided by an OpenID Connect provider and be passed as a Bearer token :

    .. code:: bash

        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ


    To validate signature, the publics keys are retrieved by fetching the issuer URL at ``/.well-known/openid-configuration`` and are store in cache for further use.

    :return: The claims contained in the JWT body.
    :rtype: dict
    :raises apicore.Http401Exception: If they is no Authorization header.
    :raises apicore.Http403Exception: If Authorization header is not valid.
    """

    token = request.args.get('token')
    if not token:
        # Authorization required
        if "Authorization" not in request.headers:
            raise Http401Exception("Neither Authorization header nor 'token' query parameter are present")

        # Get JWT from HTTP headers
        auth = request.headers.get("Authorization").split()
        if len(auth) is not 2 and auth[0] is not "Bearer":
            raise Http403Exception("Malformed Authorization HTTP Header : format MUST match Bearer TOKEN.")

        token = auth[1]

    # Find the token issuer
    try:
        tmp = jwt.get_unverified_claims(token)
        kid = jwt.get_unverified_header(token).get('kid')
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
    key = cache.get("{}@{}".format(issuer, kid))
    if not key:
        Logger.info("Caching keys for issuer '{}'".format(issuer))
        oidcConf = getJSON("{}/.well-known/openid-configuration".format(issuer))
        keys = getJSON(oidcConf.get("jwks_uri")).get("keys")
        # Cache expires in 365 or less day depending on 'exp' attribute of keys
        ts = time.mktime(datetime.datetime.utcnow().timetuple()) + (365 * 24 * 60 * 60)  # timespamp now + 365days
        for k in keys:
            expire = k.get('exp', int(ts))
            kkid = k.get('kid')

            # convert timespam from ms to s
            if expire > 4000000000:
                expire = expire // 1000

            cache.set("{}@{}".format(issuer, kkid), k, expire)
            key = cache.get("{}@{}".format(issuer, kid))

    try:
        userProfile = jwt.decode(token, key, options={"verify_aud": False, "verify_iss": False, "verify_sub": False, "verify_exp": config.tokenExpire})
        return userProfile
    except ExpiredSignatureError as ex:
        raise Http403Exception(str(ex), True)
    except JWTError as ex:
        raise Http403Exception(str(ex))


def getJSON(url):
    data = urlopen(url).read().decode("utf-8")
    return json.loads(data)
