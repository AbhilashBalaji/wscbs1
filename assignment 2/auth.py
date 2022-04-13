from tokenize import String
from xmlrpc.client import Boolean
import jwt
from time import time
# Uses pyjwt library.
SECRET="abc" # dont tell anybody lol
ALGORITHM="HS256"
EXPIRY=60 #in seconds

class Token:
    def __init__(self) -> None:
        self.secret = SECRET
        self.algorithm = ALGORITHM
        self.header = {'alg' : str(ALGORITHM)}
        self.expiry = int(EXPIRY)

    def verifyToken(self,token) -> Boolean:
        try:
            claims = jwt.decode(token,self.secret,self.algorithm)        
            # {'user_id': '123', 'expires': 1649870989.100877}
            if claims['expires'] < time() :
                return False            
            else :
                return True
        except:
            return False

    def createToken(self,userid) -> String:
        payload = {
            "user_id" : userid,
            "expires" : time() + self.expiry 
        }
        try:
            token = jwt.encode(payload,SECRET,ALGORITHM)
        except:
            return ""
        return token


# if __name__ == '__main__':
#     t = Token()
#     s = t.createToken("123")
#     print(t.verifyToken(s))