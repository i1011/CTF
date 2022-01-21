import os
enc = open('wannasleeeeeeep.txt.enc', 'rb').read()
enc, key = enc[:-4], enc[-4:]
print(len(enc))

mp = [None] * 16
for b in range(16):
    with open('tmp.txt', 'wb') as f:
        f.write(key + bytes([b * 0x11]) * len(enc))
    os.system('./wannaSleep_revenge.exe tmp.txt')
    mp[b] = open('tmp.txt.enc', 'rb').read()
    os.remove('tmp.txt.enc')
    os.remove('tmp.txt')

dec = open('wannasleeeeeeep.txt', 'wb')
dec.write(key)
for x in range(4, len(enc)):
    hb = enc[x] // 16
    lb = enc[x] % 16
    for y in range(16):
        if mp[y][x] // 16 == hb:
            hb = y
            break
    for y in range(16):
        if mp[y][x] % 16 == lb:
            lb = y
            break
    dec.write(bytes([hb * 16 + lb]))
