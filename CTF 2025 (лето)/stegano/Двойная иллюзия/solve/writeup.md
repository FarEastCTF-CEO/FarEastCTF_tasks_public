# Решение

## 1. Достаём подсказку из house.jpg (RARJPEG)

В `house.jpg` после маркера конца JPEG (`FF D9`) дописан RAR-архив.

1) Найдите смещение сигнатуры RAR:
```bash
grep -aob "Rar!" house.jpg
```
2) Вырежьте архив (смещение в моём случае `743699`):
```bash
dd if=house.jpg of=hidden.rar bs=1 skip=743699
```
3) Откройте `hidden.rar` (WinRAR/7-Zip) и достаньте `1.txt`.

Внутри строка:
```text
gyxocgeys:bifyplwix
```

## 2. Дешифруем Цезаря

Подсказка говорит про сдвиг на 20 назад (то же самое, что +6 вперёд):
```python
import string

alphabet = string.ascii_lowercase
s = "gyxocgeys:bifyplwix"
shift = 6  # -20 mod 26
print("".join(alphabet[(alphabet.index(c)+shift)%26] if c in alphabet else c for c in s))
```

Получаем:
```text
meduimkey:holevrcod
```

## 3. Извлекаем флаг из field.png

Откройте **OpenPuff** -> **Unhide**, выберите `field.png` и используйте полученный ключ (обычно достаточно первой части `meduimkey`, если утилита просит несколько паролей - используйте обе части как пароли).

После извлечения получится файл с флагом.

**Флаг:** `FECTF{hardanswer}`