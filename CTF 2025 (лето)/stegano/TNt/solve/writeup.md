# Решение

В PNG есть вспомогательные чанки `tEXt`. Автор разложил флаг по частям в чанках `PART1..PART9`.

1) Вытащите все `tEXt`-чанки и отсортируйте по номеру PART.
2) Склейте значения в одну строку.
3) Сделайте URL-decoding (встречается `%7B` и `%7D`).

Пример на Python:

```python
import struct, re, urllib.parse

data = open("TNt.png", "rb").read()
assert data[:8] == b"\x89PNG\r\n\x1a\n"

pos = 8
parts = {}

while pos < len(data):
    length = struct.unpack(">I", data[pos:pos+4])[0]
    ctype = data[pos+4:pos+8]
    chunk = data[pos+8:pos+8+length]
    pos += 12 + length

    if ctype == b"tEXt":
        key, value = chunk.split(b"\x00", 1)
        key = key.decode("latin1")
        value = value.decode("latin1")
        m = re.match(r"PART(\d+)", key)
        if m:
            parts[int(m.group(1))] = value

    if ctype == b"IEND":
        break

s = "".join(parts[i] for i in sorted(parts))
print(urllib.parse.unquote(s))
```

**Флаг:** `FECTF{f6a6869b6e3c175400233474611710de422aa7bc}`