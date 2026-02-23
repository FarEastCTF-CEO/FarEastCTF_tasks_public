# Решение

## 1. Находим подсказку и шифртекст в pcap

Открываем `task.pcapng` в Wireshark и смотрим HTTP ответ на запрос `/flag`.
В заголовках есть:

- `X-Hint: Key = MD5("fectf_http_leak!")`
- `Content-Type: application/octet-stream`
- `Content-Length: 32`

Тело ответа - 32 байта.

## 2. Дешифруем AES-ECB

Ключ AES-128 - это `MD5("fectf_http_leak!")`.

Пример скрипта:

```python
from Crypto.Cipher import AES
import hashlib

key = hashlib.md5(b"fectf_http_leak!").digest()

# 32 байта из HTTP response body (в hex можно взять из Wireshark)
ct = bytes.fromhex("31a9b3c67ea1c5acf23ffc69ca2b45e24815063d7da0f58f0aec60f9562e4930")

cipher = AES.new(key, AES.MODE_ECB)
pt = cipher.decrypt(ct)
print(pt.decode())
```

## Флаг

`FECTF{http__h3adersS__fFlL@@gG!}`
