# Решение

В `Keys.txt` даны два RSA модуля `n1` и `n2` и публичная экспонента `e`.
В `Ciphertext.txt` дан шифртекст `c`, зашифрованный на ключе `(n1, e)`.

Уязвимость: оба модуля сгенерированы с общим простым множителем `p`, поэтому:
`p = gcd(n1, n2)`.

Далее:
- `q = n1 / p`
- `phi = (p-1)(q-1)`
- `d = e^{-1} mod phi`
- `m = c^d mod n1`
- декодируем `m` как байты и получаем строку `rsa_attack_success`.

Пример скрипта:

```python
from math import gcd

n1 = 145893354580239595797239055840865340549991530981886217232629
n2 = 211801022148947775149575855784562820885631950745758150089523
e  = 17
c  = 58387981718199206244083820873656660313079074573909247195395

p = gcd(n1, n2)
q = n1 // p
phi = (p - 1) * (q - 1)

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

_, x, _ = egcd(e, phi)
d = x % phi

m = pow(c, d, n1)
pt = m.to_bytes((m.bit_length() + 7) // 8, "big").decode()
print(pt)
print("FECTF{" + pt + "}")
```

Флаг:
`FECTF{rsa_attack_success}`