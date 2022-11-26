# still some bugs
import random
import sys
import getopt
import os


# miller rabin algorithm, time complexity O(k*polylog(n)), k is number of iterations, probability of error: 4^{-k}
def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(50): # 50 times of iteration
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(1, s):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True

# generate big prime no less than bits bits
def generate_big_prime(bits):
    while True:
        n = random.randint(2**bits, 2**(bits+20))
        if is_prime(n):
            return n

# greatest common divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# using ex_gcd algorithm to calculate the inverse of a mod n
def inv(a, n):
    def ex_gcd(a, b):
        if b == 0:
            return 1, 0
        x, y = ex_gcd(b, a % b)
        return y, x - a // b * y
    x, y = ex_gcd(a, n)
    return x % n

# generate public key and private key
def rsa_make_keys(nbits):
    bits_p = nbits // 4 + random.randint(0, nbits // 2)
    bits_q = nbits - bits_p
    p = generate_big_prime(bits_p)
    q = generate_big_prime(bits_q)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(2**bits_q, 2**(nbits+20))
        if gcd(e, phi) == 1:
            break
    d = inv(e, phi)
    return (n, e), (n, d)

# encrypt a message
def rsa_encrypt(m, key):
    n, e = key
    return pow(m, e, n)

# decrypt a message
def rsa_decrypt(c, key):
    n, d = key
    return pow(c, d, n)

# encrypt a file
def rsa_encrypt_file(inf, outf, key):
    n, e = key
    bs = (n.bit_length() + 7) // 8 # block size
    while True: # read file block by block
        m = inf.read(bs)
        if not m:
            break
        m = int.from_bytes(m, 'big')
        # m = 0xFF + (m << 8)
        c = rsa_encrypt(m, key)
        outf.write(c.to_bytes(bs, 'big'))


def rsa_decrypt_file(inf, outf, key):
    n, d = key
    bs = (n.bit_length() + 7) // 8
    while True:
        c = inf.read(bs)
        if not c:
            break
        c = int.from_bytes(c, 'big')
        m = rsa_decrypt(c, key)        
        # m = m >> 8
        outf.write(m.to_bytes((m.bit_length() + 7) // 8, 'big'))


def main():
    def usage():
        print('''
        Usage: rsa.py -g -b <bits>
                 -g : generate keys  
                 -b : bits of the key (default 1024), should be no less than 128
               rsa.py -e -i <input file> -o <output file> -k <public key file>
               rsa.py -d -i <input file> -o <output file> -k <private key file>
                 -e : encrypt
                 -d : decrypt
                 -i : input file (default input.txt)
                 -o : output file (default output.txt)
                 -k : key file
        ''')
    try:
        opts = getopt.getopt(sys.argv[1:], "-g-b:-e-d-i:-o:-k:-h")[0]
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    bits = 1024
    encrypt = -1
    gen = False
    inf = 'input.txt'
    outf = 'output.txt'
    keyf = None

    for opt, arg in opts:
        if opt == '-g':
            gen = True
        elif opt == '-b':
            if not arg.isdigit():
                print('bits should be a number')
                sys.exit(1)
            bits = int(arg)
            if bits < 128:
                print('bits should be no less than 128')
                sys.exit(1)
        elif opt == '-e':
            if encrypt == -1:
                encrypt = 1
            else:
                usage()
                sys.exit(1)
        elif opt == '-d':
            if encrypt == -1:
                encrypt = 0
            else:
                usage()
                sys.exit(1)
        elif opt == '-i':
            inf = arg
        elif opt == '-o':
            outf = arg
        elif opt == '-k':
            keyf = arg
        elif opt == '-h':
            usage()
            sys.exit(0)
            
    if encrypt == -1 and not gen:
        usage()
        sys.exit(1)
    
    if gen:
        pub, prv = rsa_make_keys(bits)
        with open('rsa.pub', 'w') as f:
            f.write(f'{pub[0]} {pub[1]}')
        with open('rsa.prv', 'w') as f:
            f.write(f'{prv[0]} {prv[1]}')
        print(f'Public key: \nn={pub[0]}\ne={pub[1]}')
        print(f'Private key: \nn={prv[0]}\nd={prv[1]}')
        print('have been saved to rsa.pub and rsa.prv')
    else:
        if not keyf:
            usage()
            sys.exit(1)
        n, e = map(int, open(keyf).read().split())
        if encrypt:
            inf = open(inf, 'rb')
            outf = open(outf, 'wb')
            rsa_encrypt_file(inf, outf, (n, e))
        else:
            inf = open(inf, 'rb')
            outf = open(outf, 'wb')
            rsa_decrypt_file(inf, outf, (n, e))
        inf.close()
        outf.close()
 

if __name__ == '__main__':
    main()