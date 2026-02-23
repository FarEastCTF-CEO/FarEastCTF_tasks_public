# Решение

Используется OpenStego (сокрытие данных в изображении с паролем).

1) Пароль - это имя файла без расширений, записанное задом наперёд.

Имя файла:
```text
321terceSylimaF
```
Разворачиваем:
```text
FamilySecret123
```

2) В OpenStego выберите `Extract Data`, укажите контейнер `321terceSylimaF.jpg.bmp` и пароль `FamilySecret123`.

3) После извлечения получится `flag.txt`.

**Флаг:** `FECTF{Grandpas_Secret_Photo_123}`