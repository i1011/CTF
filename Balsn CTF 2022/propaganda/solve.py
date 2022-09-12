import subprocess

flag = b'BALSN{____this__is______not_a_flag_______}'

answer = [9128846476475241493, 7901709191400900973, 9127969212443560833, 8731519357089725617, 4447363623394058601, 616855300804233277]
def pc(n):
    return bin(n).count('1')

def f(number):
    output = subprocess.check_output(['node', 'launcher.js', str(number)])
    return int(output[:-2])

def g(number):
    a = []
    for y in range(64):
        if (number >> y) % 2: a.append(y)
    return a

mp = [0] * 64
for x in range(64):
    mp[g(f(2 ** x))[0]] = x

s = b''
for v in answer:
    w = 0
    for x in range(64):
        w += (v >> x) % 2 << mp[x]
    assert f(w) == v
    s += w.to_bytes(8, 'little')
print(s)

