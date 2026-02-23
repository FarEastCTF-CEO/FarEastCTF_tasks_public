# Райтап: Location.db

## Идея
Файл `location.db` выглядит как база с геолокациями, но **геокодирование — ложный след**. Координаты подобраны так, чтобы при отрисовке точек на плоскости получилась надпись (marker).

## Шаг 1 — открыть базу
`location.db` — это SQLite.

```bash
sqlite3 location.db ".tables"
sqlite3 location.db "PRAGMA table_info(locations);"
```

В таблице `locations` есть `latitude` и `longitude`, но они сохранены как `TEXT` и десятичная дробь записана через **запятую**.

## Шаг 2 — достать координаты числом
Приводим строки к `REAL`: заменяем `,` на `.`.

Дополнительно удобно взять `ABS(latitude)`, т.к. все широты отрицательные и надпись иначе получается «перевёрнутой/смещённой» относительно привычного чтения.

Пример запроса:

```sql
SELECT
  CAST(REPLACE(longitude, ',', '.') AS REAL) AS lon,
  ABS(CAST(REPLACE(latitude,  ',', '.') AS REAL)) AS lat
FROM locations;
```

## Шаг 3 — визуализация (scatter)
Важный момент: выставить **одинаковый масштаб по осям** (aspect = equal), иначе буквы «размажет».

Пример на Python:

```python
import sqlite3
import matplotlib.pyplot as plt

con = sqlite3.connect("location.db")
rows = con.execute("""
SELECT
  CAST(REPLACE(longitude, ',', '.') AS REAL) AS lon,
  ABS(CAST(REPLACE(latitude,  ',', '.') AS REAL)) AS lat
FROM locations
""").fetchall()

xs = [r[0] for r in rows]
ys = [r[1] for r in rows]

plt.figure(figsize=(12, 3))
plt.scatter(xs, ys, s=40)
plt.gca().set_aspect('equal', adjustable='box')
plt.gca().invert_yaxis()  # чтобы читалось «как текст»
plt.axis('off')
plt.show()
```

После отрисовки точки складываются в строку:

`SplitCTF{MArK3R}`

## Флаг
`SplitCTF{MArK3R}`
