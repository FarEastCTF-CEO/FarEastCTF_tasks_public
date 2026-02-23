# Категория | Имя задачи
Pwn | ret

# Информация
Исполнение пользовательских 7 байт кода. Цель — прыгнуть в get_flag().

# Деплой
Вариант 1 (docker compose):
```bash
cd deploy
docker compose up --build -d
```
Вариант 2 (docker run):
```bash
cd deploy
docker build -t ret .
docker run -d -p 12340:12340 ret
```

# Выдать участникам
- public/ret
- public/ret.c

# Описание задачи
Тебе разрешили написать микро-‘шеллкод’. Всего 7 байт. Хватит ли этого, чтобы добраться до флага?

# Флаг
CTF{ret_push_ret_win}
