# Encryption

#### Introduction

Simple password encryption encryption tool

Support encryption and decryption of Casear, Vigenere and Vernam cipher and cracking Casear cipher with brute force and frequency analysis method.The cracking method is automatically selected based on the text length.

~~RSA - coming~~

#### Usage

```bash
main.py [-c][-v][-V][-e][-d][-C][-h] -i <input file> -o <output file> -k <key file>
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
```

#### Example

```bash
python3 main.py -ce -i tests/article1.txt -o output/article1_en.txt -k tests/key_Casear.txt
python3 main.py -cd -i output/article1_en.txt -o output/article1_de.txt -k tests/key_Casear.txt
diff tests/article1.txt output/article1_de.txt
python3 main.py -cC -i output/article1_en.txt -o output/article1_de.txt -k tests/key_Casear.txt
Cracking with frequency analysis, key list: [9, 23, 12]
Most probable key: 12, found 2940 words
diff tests/article1.txt output/article1_de.txt
```

```
python3 main.py -ve -i tests/article1.txt -o ou
tput/article1_en.txt -k tests/key_Vigenere.txt
python3 main.py -vd -i output/article1_en.txt -o output/article1_de.txt -k tests/key_Vigenere.txt
diff tests/article1.txt output/article1_de.txt
```

```bash
python3 main.py -Ve -i tests/article1.txt -o ou
tput/article1_en.txt -k tests/key_Vernam.txt
python3 main.py -Vd -i output/article1_en.txt -o output/article1_de.txt -k tests/key_Vernam.txt
diff tests/article1.txt output/article1_de.txt
```

