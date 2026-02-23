# Решение

## 1. Достаём данные из метаданных

В `picture_CTF.jpg` есть EXIF поля:

- `ImageDescription = 192` - намекает на AES-192.
- `XPKeywords` - UTF-16LE строка, внутри Base64.

Также внутри XMP пакета в начале файла есть:

```
id='StudyHardEng1ishIsTHeKeY'
```

Это 24 байта, подходит для AES-192.

## 2. Дешифруем AES-192 ECB

- key: `StudyHardEng1ishIsTHeKeY`
- ciphertext: Base64 из `XPKeywords`

Пример (Python):

```python
import base64
from PIL import Image
from Crypto.Cipher import AES

img = Image.open("picture_CTF.jpg")
exif = img.getexif()

b64 = exif[40094].decode("utf-16le").rstrip("\x00")  # XPKeywords
ct = base64.b64decode(b64)

key = b"StudyHardEng1ishIsTHeKeY"  # 24 bytes
cipher = AES.new(key, AES.MODE_ECB)
print(cipher.decrypt(ct).decode())
```

## Флаг

`FECTF{_Nuc1ear_P0weR_PlaNt_192_}`
