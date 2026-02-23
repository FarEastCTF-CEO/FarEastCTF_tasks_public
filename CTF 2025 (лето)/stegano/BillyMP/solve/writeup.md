# Решение

Файл - BMP, но в заголовке перепутаны ширина и высота. Из-за этого часть просмотрщиков показывает мусор.

## 1. Меняем местами Width и Height

В большинстве BMP (BITMAPINFOHEADER) ширина и высота лежат по смещениям 18 и 22 (по 4 байта, little-endian). Нужно их поменять местами.

Пример фикса на Python:

```python
import struct

data = bytearray(open("billy_with_flag.bmp", "rb").read())

# DIB header size
dib = struct.unpack_from("<I", data, 14)[0]
if dib == 12:
    # BITMAPCOREHEADER (16-bit)
    w = struct.unpack_from("<H", data, 18)[0]
    h = struct.unpack_from("<H", data, 20)[0]
    struct.pack_into("<H", data, 18, h)
    struct.pack_into("<H", data, 20, w)
else:
    # BITMAPINFOHEADER (32-bit)
    w = struct.unpack_from("<i", data, 18)[0]
    h = struct.unpack_from("<i", data, 22)[0]
    struct.pack_into("<i", data, 18, h)
    struct.pack_into("<i", data, 22, w)

open("fixed.bmp", "wb").write(data)
print("saved fixed.bmp")
```

После этого `fixed.bmp` корректно открывается, и на изображении виден флаг.

**Флаг:** `FECTF{84d08f82d027c551d5b1d69ddef9a24890ebf6fc}`