#!/usr/bin/env bash
set -euo pipefail
# Пример запуска сервиса как TCP-челленджа на порту 8080 через socat
# Требуется: socat
chmod +x ./admin1
exec socat TCP-LISTEN:8080,reuseaddr,fork EXEC:"./admin1",pty,stderr
