from auth import Token

t = Token()
t1 = t.createToken("hi123")
s = t.verifyToken(t1,"h123")
print(s)