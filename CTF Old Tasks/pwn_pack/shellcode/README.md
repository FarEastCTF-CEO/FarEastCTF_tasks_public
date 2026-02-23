# Категория | Имя задачи
Pwn | shellcode

# Информация
Исполнение пользовательских 40 байт кода. Флаг лежит в ./flag.txt, нужно прочитать его самостоятельно.

# Деплой
Вариант 1 (docker compose):
```bash
cd deploy
docker compose up --build -d
```
Вариант 2 (docker run):
```bash
cd deploy
docker build -t shellcode .
docker run -d -p 19999:19999 shellcode
```

# Выдать участникам
- public/shellcode
- public/shellcode.c

# Описание задачи
Функции, печатающей флаг, больше нет. Зато тебе дали больше места для кода. Время вспомнить syscalls.

# Флаг
CTF{shellcode_read_the_flag}
