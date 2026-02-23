# Решение

## 1. Декодируем Unicode code points

В `U+.txt` записаны кодовые точки Unicode в hex:

```
005A 0073 0076 0054 0068 0073 005F 0043 007A 004C 005F 0056 0070 0065 0076 004B 0075 0070 006C
```

Переводим каждое значение `0x????` в символ и получаем строку:

```
ZsvThs_CzL_VpevKupl
```

Пример (Python):

```python
data = "005A 0073 0076 ...".split()
s = "".join(chr(int(x, 16)) for x in data)
print(s)
```

## 2. Сдвиг Цезаря (ROT7 назад)

По условию/подсказке дальше применяется ROT7. Для расшифровки делаем сдвиг на `-7` для латиницы:

```python
def caesar(s, shift):
    out = []
    for ch in s:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)

print(caesar("ZsvThs_CzL_VpevKupl", -7))
```

Получаем:

```
SloMal_VsE_OixoDnie
```

## Флаг

`FECTF{SloMal_VsE_OixoDnie}`
