import argparse
from math import gcd
from random import randint
from prime_utils import generate_prime, modinv
# from memory_profiler import profile


def int_to_string(int_string: int) -> str:
    '''Odkodowanie utf-8'''
    byte_string = int_string.to_bytes((int_string.bit_length() + 7) // 8, 'big')
    return str(byte_string, 'utf-8')


def int_from_string(string: str) -> int:
    '''Kodowanie utf-8'''
    byte_string = bytes(string, 'utf-8')
    return int.from_bytes(byte_string, 'big')

# @profile
def generate_keys(bit_size):
    '''Generator kluczy'''
    p = generate_prime(bit_size)
    q = generate_prime(bit_size)
    while p == q:
        q = generate_prime(bit_size)
    n = p * q
    phi = (p - 1) * (q - 1)

    # e tż. e < phi i wzglednie pierwsza z phi
    e = randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = randint(2, phi - 1)

    # d - inwersja e mod phi
    d = modinv(e, phi)
    public_key = (e, n)
    private_key = (d, n)

    # Zapis klucza publicznego
    with open('key.pub', 'w+') as f:
        f.write(str(public_key))

    # Zapis klucza prywatnego
    with open('key.prv', 'w+') as f:
        f.write(str(private_key))


def encrypt(message: str, public_key: tuple) -> int:
    '''Szyfrowanie kluczem publicznym'''
    e, n = public_key
    int_message = int_from_string(message)
    ciphertext = pow(int_message, e, n)
    return ciphertext


def decrypt(ciphertext: int, private_key: tuple) -> str:
    '''Odszyfrowanie kluczem prywatnym'''
    d, n = private_key
    int_message = pow(ciphertext, d, n)
    message = int_to_string(int_message)
    return message


def main():

    parser = argparse.ArgumentParser(description='RSA cryptosystem')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--gen-keys", metavar="key_lenght", type=int, default=128,
                       help="generate crypto keys")
    group.add_argument("--encrypt", metavar="message", help="encrypt message")
    group.add_argument("--decrypt", metavar="ciphertext", help="decrypt message")
    args = parser.parse_args()

    if args.gen_keys:
        generate_keys(args.gen_keys)

    elif args.encrypt:
        with open('key.pub') as f:
            key = eval(f.read())
        ciphertext = encrypt(args.encrypt, key)
        print(ciphertext)

    elif args.decrypt:
        with open('key.prv') as f:
            key = eval(f.read())
        try:
            cipher = int(args.decrypt)
        except ValueError:
            print('encrypted message should contain only digits')
            raise
        try:
            message = decrypt(cipher, key)
        except UnicodeDecodeError:
            print('cannot decrypt with current private key')
            raise
        print(message)

main()