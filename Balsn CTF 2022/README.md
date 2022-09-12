# Balsn CTF 2022
### welcome
簽到題。Flag 是網站圖片上的文字。

### my first app
題目是一個用 Next.js 寫的網站。Flag 放在 `globalVars.FLAG` ，但定義後並未在其他地方使用。

注意到 Next.js （和許多現代的框架）會在前端渲染網頁內容，`globalVars` 有機會被傳送到前端。在所有 javascript 檔案裡搜尋 `BALSN{` 便能找到 `BALSN{hybrid_frontend_and_api}`。

### Health Check 1
題目是一個看起來什麼也沒有的網站，沒有提供 source code。

觀察 response header 會發現網站使用 Uvicorn，因此能進一步（用搜尋引擎）猜到有利用 FastAPI，依據[官方文件](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls)得到 `/docs` 的路徑，可列出所有 api 的說明。

其中 `/new` 的功用是上傳包含 `run` 的 zip file，`run` 是可執行的 script 或 binary。伺服器每三十秒會執行 `run`。接著在 `../../` 得到以下檔案：

```
total 40
drwxrwxr-x  4 healthcheck uploaded 4096 Sep  3 14:43 .
drwx------  8 healthcheck uploaded 4096 Sep  3 14:43 ..
-rw-r--r--  1 healthcheck uploaded   62 Sep  3 13:55 Dockerfile
drwxr-xr-x  2 healthcheck uploaded 4096 Sep  3 14:43 __pycache__
-rw-r--r--  1 healthcheck uploaded 2892 Sep  3 13:52 apiserver.py
-rw-r--r--  1 healthcheck uploaded 2013 Sep  3 14:39 background.py
drwx--x--x 57 healthcheck uploaded 4096 Sep  3 15:58 data
-r--r-----  1 healthcheck uploaded   50 Sep  3 13:58 flag1.py
-r--r-----  1 healthcheck uploaded   35 Sep  3 13:58 flag2
-rwx------  1 healthcheck uploaded  497 Sep  3 13:58 launch.sh
```
我們可以取得 source code，不幸的是，`run` 以 `nobody` 執行，無法讀取 flag1 和 flag2。
```
total 20
drwxr-xr-x 2 healthcheck uploaded    4096 Sep  3 14:43 .
drwxrwxr-x 4 healthcheck uploaded    4096 Sep  3 14:43 ..
-rw-r--r-- 1 healthcheck healthcheck 3090 Sep  3 14:43 apiserver.cpython-310.pyc
-rw-r--r-- 1 healthcheck healthcheck 1928 Sep  3 14:43 background.cpython-310.pyc
-rw-r--r-- 1 healthcheck uploaded     172 Sep  3 14:43 flag1.cpython-310.pyc
```
然而，`__pycache__` 和底下的檔案有開放讀取，可從`flag1.cpython-310.pyc` 中取得 flag。

`BALSN{y37_4n0th3r_pYC4ch3_cHa1leN93???}`

### Health Check 2
接續前題。
`background.py` 裡能找到以下段落：
```python=
if 'docker-entry' in os.listdir(path_name):
    # experimental
    container_name = path_name.name + random.randbytes(8).hex()
    await asyncio.create_subprocess_shell(f'sleep 60; docker kill {container_name} &')
    await asyncio.create_subprocess_shell(f'sudo chmod -R a+rwx {path_name}; cd {path_name}; chmod a+x ./docker-entry; docker run --rm --cpus=".25" -m="256m" -v=$(realpath .):/data -u=user -w=/data --name {container_name} sandbox /data/docker-entry')
else:
    await asyncio.create_subprocess_shell(f'sudo chmod -R a+rwx {path_name}; cd {path_name}; sudo -u nobody timeout --signal=KILL 60 ./run')
```
Zip 裡有 `docker-entry` 會執行上面的分支。Api 文件沒提到這個功能，所以很可能有問題。不過看完後暫時沒有想法。

```python=
@app.get('/{dir_name}')
async def get_status(dir_name: str):
    file = data_path / dir_name / 'status.json'
    if not file.resolve().is_relative_to((data_path / dir_name).resolve()):
        return HTTPException(404, detail='no status')
    try:
        with open(file, 'r') as fp:
            return fp.read()
    except:
        return HTTPException(404, detail='no status')
```
接著看 api 的寫法，明顯是在防止 symbolic link，但實作上有 TOCTOU race condition，於是嘗試利用。

```bash=
#!/bin/bash
while :; do
    ln -sf status.json status.json
    ln -sf ../../flag2 status.json
done
```
接著跑 `while :; do curl $ENDPOINT; done`。指到 `status.json` 會回傳 `Internal Error`，指到 `flag2` 會回傳 `no status`，實測後在 100 次 request 內能拿到 flag。

`BALSN{d0cK3r_baD_8ad_ro07_B4d_b@d}`

Intended solution 是在 docker 裡建立 suid binary，讓下一次 `run` 的執行能提取權限。
### Flag Market 1
這題的架構是有個開放連線的服務，需透過該服務去存取 backend。Backend 是一個 python 伺服器。

`xinetd-flag1` 提示 flag1 是在 backend 的一項服務。
```
service backend-flag1
{
...
        server = /backend/run_flag1.sh
...
        user = backend
	port = 31337
...
}

```
```bash
#!/bin/bash

echo $FLAG1
```
`run_flag1.sh` 的內容很單純，只要將連線的 port 從 python 伺服器換成 flag1 就能拿到 flag。

```c=
void connection_handler(int sock_fd)
{
    char request[MAX_REQ_BUF] = {};
    char method[MAX_BUF] = {};
    char path[MAX_BUF] = {};
    char port[MAX_BUF] = {};
    char host[MAX_BUF] = {};
    ...
    snprintf(host, MAX_BUF, "%s", BK_HOST);
    snprintf(port, MAX_BUF, "%d", BK_PORT);

    reqLen = read_input(sock_fd, request, MAX_REQ_BUF);

    n = sscanf(request, "%s /%s HTTP/1.1", method, path);
    ...
```
`sscanf` 有 buffer overflow 的問題，傳送 `"A /" + "A" * MAX_BUF + "31337"` 能蓋掉 port。

### Flag Market 2
`backend.py` 要求構造滿足若干條件的 request 。基本上可以抄 `curl -v` 的輸出。比較麻煩的是 payload 裡要有 ascii 0~255 的所有字元，url encode 後可能會超過 `MAX_REQ_BUF = 1024`。經過嘗試，很多不可視字元不須編碼也能正確解析，因此得以壓到 1024 個字元內。
### Cairo Reverse
```
# Declare this file as a StarkNet contract.
%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@view
func get_flag{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
}(t:felt) -> (res : felt):
    if t == /* Censored */:
        return (res=0x42414c534e7b6f032fa620b5c520ff47733c3723ebc79890c26af4 + t*t)
    else:
        return(res=0)
    end
end
```
給編譯完的結果，求 t 的數值。

隨便輸入 t ，比對編譯結果。
```
39c39
<             "0x800000000000010fffffffffffffffffffffffffffffff00000000000000002",
---
>             "0x800000000000010fffffffffffffffffffffffffffe2919e3d696087d12173e",
106c106
<                         "end_col": 32,
---
>                         "end_col": 38,
```
將 t 的長度補到 `end_col` 一樣，`t = 0xfffffffffffffffffffffff` 的結果是：
```
39c39
<             "0x800000000000010fffffffffffffffffffffffff00000000000000000000002",
---
>             "0x800000000000010fffffffffffffffffffffffffffe2919e3d696087d12173e"
```
多試幾個數字可以發現除了末位外是將 t 和一個大常數 xor，最後得到 `t = 0x001d6e61c2969f782ede8c3`。

`BALSN{read_data_from_cairo}`

### Propaganda
用 `wasm2c` 反編譯後會得到很多式子，乍看下可以耗費一番苦功用 z3 解，但試了幾個輸入後發現程式只是將 bit 的順序重新排列，

`BALSN{ya_sdelal_etot_challenge_za_den_do_ctf}`
### Yet another RSA with hint

正常的 RSA， p 和 q 的 bit length 一樣，提示 p 在 2 進位 ~ 199 進位下的 digit sum。

注意到 N 在 K 進位下的 digit sum 相當於除以 K - 1 的餘數，依中國剩餘定理得到 p = r (mod m)，其中 m 是個很大的數字。

如果 m > p ， r 就是答案了，但 m 還不夠大，這個情況相當於洩漏 p 的低位資訊，可利用 Coppersmith's attack。實作上使用 sage 的 `small_roots` 即可。
