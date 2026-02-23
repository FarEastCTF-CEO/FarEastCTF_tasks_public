# Решение

В PNG размер хранится в чанке **IHDR**: ширина и высота - это по 4 байта (big-endian) сразу после сигнатуры `IHDR`.

У `tree.png` высота в заголовке занижена, хотя в IDAT реально закодировано гораздо больше строк.

## 1. Исправляем высоту

Фактическое число строк в данных - `65375` (0x0000FF5F).

Замените 4 байта высоты в IHDR на:
```text
00 00 FF 5F
```

Это можно сделать в любом hex-редакторе. После правки откройте PNG и прокрутите вниз - появится строка в base58.

## 2. Декодируем base58

Строка декодируется в флаг. Пример на Python:

```python
alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
s = "fJPfwyLwcvcFry29EJ1bpax"

num = 0
for ch in s:
    num = num * 58 + alphabet.index(ch)

b = num.to_bytes((num.bit_length() + 7) // 8, "big")
print(b.decode("utf-8"))
```

**Флаг:** `FECTF{sTecREreEt}`