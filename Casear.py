import sys
from collections import Counter


def init_key(key):
    try:
        key = int(key)
    except:
        print("Key should be a number")
        sys.exit(1)
    key = key % 26
    return key

def encrypt(text, outf, key):
    key = init_key(key)
    out = ""
    for c in text:
        if not c.encode('utf-8').isalpha():
            out += c
            continue
        if c.isupper():
            out += chr((ord(c) - 65 + key) % 26 + ord('A'))
        else:
            out += chr((ord(c) - 97 + key) % 26 + ord('a'))
    outf.write(out)


def decrypt(text, outf, key):
    encrypt(text, outf, '-'+key)

def import_words():
    words = set()
    with open("data/words.txt", 'r') as f:
        for line in f:
            words.add(line.strip())
    return words

def crack(text, outf):
    # https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    # freq = {'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02, 'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49, 'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.10, 'z': 0.07}
    count = Counter(text.lower())
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    fir_freq, sec_freq, thi_freq = sorted_count[0][0], sorted_count[1][0], sorted_count[2][0]
    words = import_words()
    ou = [""] * 26
    max_cnt, best_key = 0, 0
    if len(text) > 1000:
        key_list = [ord(fir_freq) - ord('e'), ord(sec_freq) -
                    ord('t'), ord(thi_freq) - ord('a')]
        for i in range(3):
            key_list[i] = key_list[i] % 26
        print(f"Cracking with frequency analysis, key list: {key_list}")
    else:
        key_list = [i for i in range(26)]
        print(f"length = {len(text)}, Cracking with brute force")
    for key in key_list:
        out = ""
        cur_word = ""
        cnt = 0
        for c in text:
            if not c.isalpha():
                if cur_word in words:
                    cnt += 1
                cur_word = ""
                out += c
                continue
            ch = chr((ord(c) - ord('A') - key) % 26 + ord('A'))
            if c.islower():
                ch = chr((ord(c) - ord('a') - key) % 26 + ord('a'))
            out += ch
            cur_word += ch
        if cur_word in words:
            cnt += 1
        if cnt > max_cnt:
            max_cnt = cnt
            best_key = key
        ou[key] = out
    if max_cnt > 10:
        print(f"Most probable key: {best_key}, found {max_cnt} words")
        outf.write(ou[best_key])
    else:
        print("Too few words found, output all possible results")
        for i in range(26):
            outf.write(f"key: {i}\n{ou[i]}\n")
