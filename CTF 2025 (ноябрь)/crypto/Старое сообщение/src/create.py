import pyotp
import base64
import time

totp = pyotp.TOTP(base64.b32encode(b'very_secret_key_for_crypt'), 10)
secret_key = totp.at(1183806001) # 7 July 2007 г., 11:02:58
print(secret_key)
print(type(secret_key))

def xor_encrypt_decrypt(text, key):
    """
    Шифрует или дешифрует строку, используя операцию XOR с заданным ключом.
    """
    # Приводим ключ к списку байтов, повторяя его до длины текста
    key_bytes = [k for k in key * (len(text) // len(key) + 1)][:len(text)]
    key_bytes = ''.join(key_bytes).encode('utf-8')
    print(key_bytes)
    text = text.encode('utf-8')

    encrypted_text = bytes([text[i] ^ key_bytes[i] for i in range(len(text))])

    return encrypted_text


flag = "FECTF{Crypt0_0ld_t1me}"


# Шифрование
encrypted = xor_encrypt_decrypt(flag, secret_key)
print(f"Зашифрованный текст: {encrypted}")
print(f"Зашифрованный текст: {encrypted.decode('utf-8')}")

with open('encrypted_message', 'wb') as f:
    f.write(encrypted)