# Категория | Имя задачи
Pwn | overflow2

# Информация
Overflow как в overflow1, но требуется записать в is_root точное значение 0x12345678 (little-endian).

# Деплой
Вариант 1 (docker compose):
```bash
cd deploy
docker compose up --build -d
```
Вариант 2 (docker run):
```bash
cd deploy
docker build -t overflow2 .
docker run -d -p 16555:16555 overflow2
```

# Выдать участникам
- public/overflow2
- public/overflow2.c

# Описание задачи
Проверка стала строже: теперь нужен правильный ключ. Только вот ключ лежит прямо за буфером…

# Флаг
CTF{overflow2_little_endian}
