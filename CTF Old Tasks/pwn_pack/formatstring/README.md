# Категория | Имя задачи
Pwn | formatstring

# Информация
Format string: printf(user_input, ...) позволяет вывести secret (8-й аргумент) и затем угадать его.

# Деплой
Вариант 1 (docker compose):
```bash
cd deploy
docker compose up --build -d
```
Вариант 2 (docker run):
```bash
cd deploy
docker build -t formatstring .
docker run -d -p 40003:40003 formatstring
```

# Выдать участникам
- public/formatstring
- public/formatstring.c

# Описание задачи
Сервис приветствует пользователей… но слишком доверяет их именам. Может, имя само подскажет секрет?

# Флаг
CTF{formatstring_printf_gotcha}
