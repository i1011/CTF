from Crypto.Util.number import *
import os


blen = 256

def rsa(p: int, q: int, message: bytes):
    n = p * q
    e = 65537
    
    pad_length = n.bit_length() // 8 - len(message) - 2 # I padded too much
    message += os.urandom(pad_length)
    print(message)
    m = bytes_to_long(message)
    return (n, pow(m, e, n))

def level1(message1: bytes, message2: bytes):
    global p1, p2
    while True:
        p1 = getPrime(blen) # 512-bit number
        p2 = (p1 - 1) // 2
        if isPrime(p2):
            break

    q1 = getPrime(blen)
    q2 = getPrime(blen)

    return rsa(p1, q1, message1), rsa(p2, q2, message2)

def level2(message1: bytes, message2: bytes):
    while True:
        p1 = getPrime(blen) # 512-bit number
        p2 = (p1 + 1) // 2
        if isPrime(p2):
            break

    q1 = getPrime(blen)
    q2 = getPrime(blen)

    return rsa(p1, q1, message1), rsa(p2, q2, message2)

flag = b'A' * 44
assert len(flag) == 44
l = len(flag) // 4
# m1, m2, m3, m4 = [flag[i * l: i * l + l] for i in range(4)]
# c1, c2 = level1(m1, m2)
# c3, c4 = level2(m3, m4)
exec(open('output.txt', 'r').read())
print(f'{c1 = }')
print(f'{c2 = }')
print(f'{c3 = }')
print(f'{c4 = }')

import math
n1, n2 = c1[0], c2[0]
POOL = 10
ls = [pow(x + 1, n2 * 2, n1) - 1 for x in range(POOL)]
for x in range(POOL):
    for y in range(x + 1, POOL):
        g = math.gcd(ls[x], ls[y])
        if g == 1 or g == n1 or n1 % g: continue
        p1, q1 = g, n1 // g
        break
assert p1 * q1 == n1
p2 = (p1 - 1) // 2
q2 = n2 // p2
assert p2 * q2 == n2
m1 = pow(c1[1], inverse(65537, (p1 - 1) * (q1 - 1)), n1)
m2 = pow(c2[1], inverse(65537, (p2 - 1) * (q2 - 1)), n2)

print(long_to_bytes(m1)[:11].decode(), end='')
print(long_to_bytes(m2)[:11].decode())
