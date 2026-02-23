# Категория | Имя задачи
Pwn | arbitrary_write

# Информация
Один произвольный write в память: нужно найти адрес VAR и записать 0x00defaced.

# Деплой
Вариант 1 (docker compose):
```bash
cd deploy
docker compose up --build -d
```
Вариант 2 (docker run):
```bash
cd deploy
docker build -t arbitrary_write .
docker run -d -p 40002:40002 arbitrary_write
```

# Выдать участникам
- public/arbitrary_write
- public/arbitrary_write.c

# Описание задачи
Тебе дали ручку, которая пишет куда угодно. Осталось понять, куда именно надо поставить подпись, чтобы открылась дверь.

# Флаг
CTF{arbitrary_write_symbol_table}
