from auth import Token

t = Token()
t1 = t.createToken("hi123")
print(t.getUserIdfromToken(t1))