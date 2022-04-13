from auth import Token

t = Token()
t1 = t.createToken(123)
s = t.verifyToken(t1)
print(s)