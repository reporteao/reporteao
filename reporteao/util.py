import random, string

def uuid():
    letras = string.ascii_uppercase + string.ascii_lowercase
    uuid = ''
    for _ in range(0, 16):
        uuid += random.choice(letras)
    return str(uuid)
