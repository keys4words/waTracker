import bcrypt

pwd = 'something'.encode('utf-8')
hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
print('initial: ' + str(pwd))
print('hashed:  ' + str(hashed_pwd))

if bcrypt.checkpw('something'.encode('utf-8'), hashed_pwd):
    print('Match')
else:
    print('Not match')