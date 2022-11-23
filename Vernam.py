# Vernam cipher

def encrypt(text, outf, key):
    while len(key) < len(text):
        key += key
    key = key[:len(text)]
    # print(len(list(text)), list(text), list(key))
    out = bytes([a ^ b for a, b in zip(text, key)])
    outf.write(out)

def decrypt(text, outf, key):
    encrypt(text, outf, key)
    