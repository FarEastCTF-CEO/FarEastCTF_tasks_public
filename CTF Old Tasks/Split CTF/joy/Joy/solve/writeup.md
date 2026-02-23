# Joy — writeup

## Идея
Файл `joy_25.xlsx` выглядит как обычная таблица, но после сортировки порядок символов в строке потерян.

Ключевой факт: **`.xlsx` — это ZIP-архив** с набором XML-файлов. Excel хранит строки в таблице `xl/sharedStrings.xml`, а в листах (`xl/worksheets/sheet*.xml`) в ячейках записывает **индексы** на эти строки.

После сортировки значения в ячейках поменялись местами, но **индексы на строки остались** — по ним можно восстановить исходный текст.

## Решение (концептуально)
1. Переименовать `joy_25.xlsx` в `joy_25.zip` и распаковать.
2. Открыть:
   - `xl/sharedStrings.xml` — таблица строк (символов),
   - `xl/worksheets/sheet1.xml` — ячейки листа и их индексы `<v>...</v>`.
3. Собрать все индексы из `sheet1.xml`, отсортировать их по возрастанию и заменить на символы из `sharedStrings.xml`.
   - Если какой-то индекс встречается несколько раз (как тут для `s`), он просто добавится в строку столько же раз.

## Скрипт (Python)
```python
import zipfile
import xml.etree.ElementTree as ET

xlsx = "joy_25.xlsx"

with zipfile.ZipFile(xlsx) as z:
    shared = ET.fromstring(z.read("xl/sharedStrings.xml"))
    sheet1 = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))

ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

# Таблица строк: index -> symbol
strings = [si.find(".//m:t", ns).text for si in shared.findall("m:si", ns)]

# Индексы из ячеек (их может быть больше, чем unique strings!)
idxs = [int(c.find("m:v", ns).text) for c in sheet1.findall(".//m:sheetData//m:c", ns)]

flag = "".join(strings[i] for i in sorted(idxs))
print(flag)
```

Вывод:
```
SplitCTF{ss0_e@y}
```

## Флаг
`SplitCTF{ss0_e@y}`
