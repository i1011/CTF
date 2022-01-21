import random

class MyRandom:
    def __init__(self, a, b):
        self.n = 256
        self.a = a
        self.b = b

    def random(self):
        tmp = self.a
        self.a, self.b = self.b, (self.a * 69 + self.b * 1337) % self.n
        tmp ^= (tmp >> 3) & 0xde
        tmp ^= (tmp << 1) & 0xad
        tmp ^= (tmp >> 2) & 0xbe
        tmp ^= (tmp << 4) & 0xef
        return tmp

class TruelyRandom:
    def __init__(self, a1, b1, a2, b2, a3, b3):
        self.r1 = MyRandom(a1, b1)
        self.r2 = MyRandom(a2, b2)
        self.r3 = MyRandom(a3, b3)

    def random(self):
        def rol(x, shift):
            shift %= 8
            return ((x << shift) ^ (x >> (8 - shift))) & 255

        o1 = rol(self.r1.random(), 87)
        o2 = rol(self.r2.random(), 6)
        o3 = rol(self.r3.random(), 3)
        o = (~o1 & o2) ^ (~o2 | o3) ^ (o1)
        return o & 255

class TruelyRandom1:
    def __init__(self, a1, b1):
        self.r1 = MyRandom(a1, b1)

    def random(self):
        def rol(x, shift):
            shift %= 8
            return ((x << shift) ^ (x >> (8 - shift))) & 255

        o1 = rol(self.r1.random(), 87)
        o = o1
        return o & 255

class TruelyRandom3:
    def __init__(self, a3, b3):
        self.r3 = MyRandom(a3, b3)

    def random(self):
        def rol(x, shift):
            shift %= 8
            return ((x << shift) ^ (x >> (8 - shift))) & 255

        o3 = rol(self.r3.random(), 3)
        o = o3
        return o & 255

for o1 in range(2):
    for o2 in range(2):
        for o3 in range(2):
            o = (~o1 & o2) ^ (~o2 | o3) ^ (o1)
            o = o & 1
            print(f'{o1} {o2} {o3} = {o}')

flag_sequence = bytes.fromhex(open('output.txt', 'r').read())
flag_len = 36
pc = [0] * 256
for x in range(256):
    pc[x] = x % 2 + pc[x // 2]

# search a1, b1
ls1 = []
for a in range(256):
    for b in range(256):
        rng = TruelyRandom1(a, b)
        random_sequence = [rng.random() for _ in range(420)]
        eq = [pc[random_sequence[x] ^ flag_sequence[x]] for x in range(flag_len, 420)]
        if sum(eq) >= (420 - flag_len) * 8 // 8 * 6 - 100: ls1.append((a, b))
print(ls1)
a1, b1 = ls1[0]

# search a3, b3
ls3 = []
for a in range(256):
    for b in range(256):
        rng = TruelyRandom3(a, b)
        random_sequence = [rng.random() for _ in range(420)]
        eq = [pc[random_sequence[x] ^ flag_sequence[x]] for x in range(flag_len, 420)]
        if sum(eq) >= (420 - flag_len) * 8 // 8 * 6 - 100: ls3.append((a, b))
print(ls3)
a3, b3 = ls3[0]

# search a2, b2
ls = []
for a1, b1 in ls1:
    for a3, b3 in ls3:
        for a in range(256):
            for b in range(256):
                rng = TruelyRandom(a1, b1, a, b, a3, b3)
                random_sequence = [rng.random() for _ in range(420)]
                neq = [pc[random_sequence[x] ^ flag_sequence[x]] for x in range(flag_len, 420)]
                if sum(neq) == 0:
                    print(*[chr(random_sequence[x] ^ flag_sequence[x]) for x in range(flag_len)], sep='')
