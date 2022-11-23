import sys

def init_key(key, text):
    if not key.encode('utf-8').isalpha():
        print("Key should be alphabetic")
        sys.exit(1)
    
    key = key.upper()
    while len(key) < len(text):
        key += key
    return key[:len(text)]

def get_table():
    password_table = []
    for i in range(26):
        password_table.append([])
        for j in range(26):
            password_table[i].append(chr((i + j) % 26 + ord('A')))
    return password_table

def encrypt(text, outf, key):
    key = init_key(key, text)
    out = ""
    password_table = get_table()
    for i in range(len(text)):
        c = text[i]
        if not c.encode('utf-8').isalpha():
            out += c
            continue
        nc = password_table[ord(c.upper()) - ord('A')][ord(key[i]) - ord('A')]
        out += nc if c.isupper() else nc.lower()
    outf.write(out)

def decrypt(text, outf, key):
    new_key = ''
    for i in range(len(key)):
        new_key += chr(ord('A') + (26 - (ord(key[i]) - ord('A'))) % 26)
    encrypt(text, outf, new_key)