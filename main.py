import sys
import os
import getopt
import Casear
import Vigenere
import Vernam


def main():
    def usage():
        print('''
        Usage: main.py [-c][-v][-V][-e][-d][-C][-h] -i <input file> -o <output file> -k <key file>
        -c : Caesar, key should be an integer
        -v : Vigenere, key should be a string
        -V: Vernam ciphers, key should be a string
        -e : encrypt
        -d : decrypt
        -C : crack(only for Caesar)
        -i : input file(default input.txt)
        -o : output file(default output.txt)
        -k : key file(default key.txt)
        -h : help
        ''')
    try:
        opts = getopt.getopt(sys.argv[1:], "-h-c-v-C-V-e-d-k:-i:-o:")[0]
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    cipher_flag = 0
    inf, outf, keyf = "input.txt", "output.txt", "key.txt"
    encrypt = -1
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit(0)
        elif opt == "-c":
            if cipher_flag == 0:
                cipher_flag = 'c'
            else:
                usage()
                sys.exit(1)
        elif opt == "-v":
            if cipher_flag == 0:
                cipher_flag = 'v'
            else:
                usage()
                sys.exit(1)
        elif opt == "-V":
            if cipher_flag == 0:
                cipher_flag = 'V'
            else:
                usage()
                sys.exit(1)
        elif opt == "-e":
            if encrypt == -1:
                encrypt = 1
            else:
                usage()
                sys.exit(1)
        elif opt == "-d":
            if encrypt == -1:
                encrypt = 0
            else:
                usage()
                sys.exit(1)
        elif opt == "-i":
            inf = arg
        elif opt == "-o":
            outf = arg
        elif opt == "-k":
            keyf = arg
        elif opt == "-C":
            if encrypt == -1:
                encrypt = 2
            else:
                usage()
                sys.exit(1)
        else:
            usage()
            sys.exit(1)
    if not os.path.exists(inf):
        print(f"Input file {inf} does not exist")
        sys.exit(1)
    if not os.path.exists(keyf) and encrypt != 2:
        print(f"Key file {keyf} does not exist and you are not cracking")
        sys.exit(1)
    if encrypt == -1:
        print("Please specify encrypt or decrypt")
        sys.exit(1)
    if encrypt == 2 and cipher_flag != 'c':
        print("Only Caesar cipher can be cracked")
        sys.exit(1)
    if cipher_flag != 'V':
        inf = open(inf, 'r', encoding='utf-8')
        outf = open(outf, 'w', encoding='utf-8')
        keyf = open(keyf, 'r', encoding='utf-8')
    else:
        inf = open(inf, 'rb')
        outf = open(outf, 'wb')
        keyf = open(keyf, 'rb')
    
    text = inf.read()
    key = keyf.read()
    if cipher_flag == 'c':
        if encrypt == 1:
            Casear.encrypt(text, outf, key)
        elif encrypt == 0:
            Casear.decrypt(text, outf, key)
        else:
            Casear.crack(text, outf)
    elif cipher_flag == 'v':
        if encrypt == 1:
            Vigenere.encrypt(text, outf, key)
        elif encrypt == 0:
            Vigenere.decrypt(text, outf, key)
    elif cipher_flag == 'V':
        if encrypt == 1:
            Vernam.encrypt(text, outf, key)
        elif encrypt == 0:
            Vernam.decrypt(text, outf, key)
    else:
        print("Please specify a cipher")
        sys.exit(1)
    inf.close()
    outf.close()
    keyf.close()


if __name__ == '__main__':
    main()
