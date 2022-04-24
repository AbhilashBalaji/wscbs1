from tokenize import String
from xmlrpc.client import Boolean
import jwt
from time import time
from enum import Enum

# Uses pyjwt library.
SECRET = "abc"  # dont tell anybody lol
ALGORITHM = "HS256"
EXPIRY = 60 * 600000000000  # in seconds
tokens_status = Enum('tokens_status', 'time_expired user_not_matched verified unknown')


class Token:
    def __init__(self) -> None:
        self.secret = SECRET
        self.algorithm = ALGORITHM
        self.header = {'alg': str(ALGORITHM)}
        self.expiry = int(EXPIRY)

    def verifyToken(self, token, userid) -> dict:
        try:
            claims = jwt.decode(token, self.secret, self.algorithm)
            # {'user_id': '123', 'expires': 1649870989.100877}
            if claims['expires'] < time():
                return {'status': tokens_status.time_expired}
            elif claims['user_id'] != str(userid):
                return {'status': tokens_status.user_not_matched}
            else:
                return {'status': tokens_status.verified}
        except:
            return {'status': tokens_status.unknown}

    def getUserIdfromToken(self, token):
        try:
            claims = jwt.decode(token, self.secret, self.algorithm)
            return claims['user_id']
        except:
            return None

    def createToken(self, userid) -> String:
        payload = {
            "user_id": userid,
            "expires": time() + self.expiry
        }
        print("payload=",payload)
        print("payload=",SECRET)
        print("payload=",ALGORITHM)
        token = jwt.encode(payload, SECRET, ALGORITHM)
        return token

# if __name__ == '__main__':
#     t = Token()
#     s = t.createToken("123")
#     print(t.verifyToken(s))
