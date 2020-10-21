from random import randint, getrandbits


def modinv(a, m):
    '''Inwersja modularna'''
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def egcd(a, b):
    '''Rozszerzony algorytm euklidesa'''
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def miller_rabin(n, k=10):
    '''Test pierwszości Millera Rabina'''
    if n == 2:
        return True
    if n == 1 or n % 2 == 0:
        return False

    s, d = 0, n - 1
    while not d % 2:
        s += 1
        d //= 2
    assert(2**s*d == n - 1)

    def check_if_composite_using(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False  # prawdopodbnie pierwsza
        for _ in range(s):
            x = (x * x) % n  # dla każdego a^((2^i)*d)
            if x == n - 1:
                return False  # prawdopodbnie pierwsza
        return True  # złożona

    # k testów
    for i in range(k):
        a = randint(2, n-1)
        if check_if_composite_using(a):
            return False  # złożona
    return True  # prawdopodobnie piwerwsza


def generate_prime(bit_size):
    '''Generator liczb pierwszych'''
    p = getrandbits(bit_size)
    if not p % 2:  # sprawdzenie parzystości
        p += 1
    while not miller_rabin(p):  # sprawdzanie pierwszości
        p = p + 2
    return p