from requests.auth import AuthBase
import hashlib
import string
import time
import os
from calendar import timegm
import urllib

class NFSNAuth(AuthBase):
    """Signs the request to NFS.N"""
    api_key = None
    login = None

    def __init__(self, api_key=None, login=None):
        if api_key is None and self.api_key is None:
            raise KeyError("No Api key set.")
        elif self.api_key is None:
            self.api_key = api_key

        if login is None and self.login is None:
            raise KeyError("No login credentials specified")
        elif self.login is None:
            self.login = login

    def __call__(self, request):
        """Generate a hash, and set the X-NFSN Header"""
        body = ""
        if isinstance(request.body, list) and request.body:
            body = urllib.urlencode(request.body)
        elif request.body:
            body = request.body

        body_hash = hashlib.sha1(body.encode('utf8')).hexdigest()
        salt = self._gen_salt()
        timestamp = self._gen_timestamp()
        hash_string = ";".join((self.login,
                                timestamp,
                                salt,
                                self.api_key,
                                request.path_url,
                                body_hash))
        hash = hashlib.sha1(hash_string.encode('utf8')).hexdigest()
        request.headers["X-NFSN-Authentication"] = \
                ";".join((self.login, timestamp, salt, hash))
        return request

    def _gen_salt(self):
        """Generate a 16 character a-zA-Z0-9 Salt for signing"""
        chars = "".join((string.ascii_lowercase, string.ascii_uppercase, string.digits))
        return "".join([chars[x%len(chars)] for x in os.urandom(16)])

    def _gen_timestamp(self):
        """Get the current 32-bit UNIX timestamp"""
        return str(int(time.time()))
