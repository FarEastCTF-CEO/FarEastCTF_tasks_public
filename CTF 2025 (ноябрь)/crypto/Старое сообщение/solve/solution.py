import pyotp
import base64
import time

totp = pyotp.TOTP(base64.b32encode(b'very_secret_key_for_crypt'), 10)


with open('encrypted_message', 'rb') as f:
    encrypted = f.read()

start_2007 = 1167609600
end_2007 = 1199145599
start_flag = b"FECTF{"

time_key = start_2007

while time_key < end_2007:

	secret_key_number = totp.at(time_key)

	key_bytes = secret_key_number.encode('utf-8')

	encrypted_text = bytes([start_flag[i] ^ key_bytes[i] for i in range(len(start_flag))])

	if encrypted_text == encrypted[:len(start_flag)]:
		key_bytes = [k for k in secret_key_number * (len(encrypted) // len(secret_key_number) + 1)][:len(encrypted)]
		key_bytes = ''.join(key_bytes).encode('utf-8')
		print(key_bytes)
		print(time_key)
		print(bytes([encrypted[i] ^ key_bytes[i] for i in range(len(encrypted))]))
		

	time_key += 1