# Категория | Имя задачи
Pwn | overflow1

# Информация
Базовый стековый overflow через gets(): переполнение buffer перезаписывает is_root.

# Деплой
Вариант 1 (docker compose):
```bash
cd deploy
docker compose up --build -d
```
Вариант 2 (docker run):
```bash
cd deploy
docker build -t overflow1 .
docker run -d -p 31337:31337 overflow1
```

# Выдать участникам
- public/overflow1
- public/overflow1.c

# Описание задачи
Система контроля доступа сломалась: если ты сумеешь стать root — покажем секрет. Твое имя здесь явно важно…

# Флаг
CTF{overflow1_kiddy_overflow}
