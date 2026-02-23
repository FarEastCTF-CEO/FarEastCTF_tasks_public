import socket
import re
import base64
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(('localhost', 8080))  # подключемся к серверному сокету

for i in range (0, 51):
    data = sock.recv(2048) 
    print(str(data))
    result = re.findall(r'Give base64 decode string: (.+)\\n', str(data))
    dr = base64.b64decode(result[0])
    print(result[0])
    time.sleep(1)
    sock.send(dr)
    sock.send(b'\n')
    time.sleep(1)

sock.close()  # закрываем соединение
print(data)
