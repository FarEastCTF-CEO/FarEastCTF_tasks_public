import pyotp
import base64
import time

totp = pyotp.TOTP(base64.b32encode(b'very_secret_key_for_crypt'), 10)
secret_key = totp.now()

def xor_encrypt_decrypt(text, key):

    key_bytes = [k for k in key * (len(text) // len(key) + 1)][:len(text)]
    key_bytes = ''.join(key_bytes).encode('utf-8')

    text = text.encode('utf-8')

    encrypted_text = bytes([text[i] ^ key_bytes[i] for i in range(len(text))])

    return encrypted_text


flag = ""

encrypted = xor_encrypt_decrypt(flag, secret_key)

with open('encrypted_message', 'wb') as f:
    f.write(encrypted)