# Решение

В файле `secret.txt` виден нормальный английский текст, но в нем намеренно добавлены повторы букв, чтобы исказить статистику. В конце файла есть фрагмент из `{}`, `x`, но сам `x` не входит в используемый алфавит шифрования.

Идея: автор зашифровал флаг порядком символов по убыванию их частоты.

Используем алфавит:
`abcdefghijklmnopqrstuvwxyz{}_`

Шаги:
1. Считаем частоты всех символов из алфавита (регистр не важен).
2. Сортируем символы по убыванию частоты и склеиваем их в строку.
3. В получившейся строке находим подстроку от `{` до `}` - это содержимое флага.

Пример скрипта:

```python
from collections import Counter

alphabet = "abcdefghijklmnopqrstuvwxyz{}_"
text = open("secret.txt", "r", encoding="utf-8").read().lower()

freq = {ch: 0 for ch in alphabet}
for ch in text:
    if ch in freq:
        freq[ch] += 1

order = "".join(ch for ch, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True))
print(order)

start = order.index("{")
end = order.index("}", start)
print("FECTF{" + order[start+1:end] + "}")
```

Итоговый флаг:
`FECTF{wavy_sphinx}`