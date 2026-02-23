# Решение

В `ZipFile.zip` лежат три JPG.

1) `floppa_say.jpg` визуально содержит подсказку на инструмент **outguess**.
2) `floppa_hehe.jpg` содержит пароль: `3301` (его нужно использовать в outguess).
3) В `floppa_secrets.jpg` спрятан выводимый файл.

Команда для извлечения (пример):
```bash
outguess -k 3301 -r floppa_secrets.jpg secret.txt
```

В `secret.txt` будет флаг.

**Флаг:** `FECTF{thaNks_3301_for_iDea}`