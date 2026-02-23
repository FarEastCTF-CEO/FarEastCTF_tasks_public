# Райтап: Caesar cipher (шифр Цезаря)

---

## 1) Дано

По условию задания используется **шифр Цезаря**.  
Шифртекст находится во входном файле и представляет собой строку,
зашифрованную с фиксированным сдвигом по латинскому алфавиту.

---

## 2) Метод решения

Так как величина сдвига неизвестна, применяется стандартный подход:

- перебор всех возможных сдвигов от `0` до `25`;
- анализ полученных строк;
- поиск осмысленного текста и шаблона флага формата `SplitCTF{...}`.

---

## 3) Перебор сдвигов (bruteforce)

```python
import string

cipher = "Q+oqxxqz?@ k.(; rxms e,xu?OfR%hqzuAhupuAhuou$"

LOW = string.ascii_lowercase
UP  = string.ascii_uppercase

def caesar_decrypt(s, shift):
    res = ""
    for c in s:
        if c in LOW:
            res += LOW[(LOW.index(c) - shift) % 26]
        elif c in UP:
            res += UP[(UP.index(c) - shift) % 26]
        else:
            res += c
    return res

for i in range(26):
    print(i, caesar_decrypt(cipher, i))
```

---

## 4) Результат

При одном из сдвигов получается осмысленная строка,
содержащая корректный формат флага задания.

**Флаг:**

```
SplitCTF{Veni_Vidi_Vici}
```

---

## 5) Итог

- Тип шифра: **Caesar**
- Метод: перебор всех сдвигов
- Ответ: `SplitCTF{Veni_Vidi_Vici}`
