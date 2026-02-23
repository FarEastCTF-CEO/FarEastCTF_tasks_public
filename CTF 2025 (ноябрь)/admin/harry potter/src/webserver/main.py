# vuln_lfi_fixed.py
from flask import Flask, request, Response
import os
import urllib.parse

app = Flask(__name__)

# База — папка, где лежит этот скрипт (чтобы не зависеть от CWD)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def index():
    return ("Добро пожаловать на мой первый сайт!\nВы можете добавить в адресной строке /show?file=harry.txt и прочитать отрывок из Гарри Поттера\n", 200, {"Content-Type": "text/plain; charset=utf-8"})

@app.route("/show")
def show():
    filename = request.args.get("file", "")
    if not filename:
        return ("file parameter required\n", 400)

    # Декодируем URL-энкодинг
    filename = urllib.parse.unquote(filename)

    # Собираем путь и нормализуем
    joined = os.path.join(BASE_DIR, filename)
    abs_path = os.path.abspath(joined)

    # Отладка: покажем путь и существование файла если ошибка
    try:
        with open(abs_path, "rb") as f:
            data = f.read()
    except Exception as e:
        debug = (
            "DEBUG\n"
            f"requested: {filename}\n"
            f"BASE_DIR: {BASE_DIR}\n"
            f"joined: {joined}\n"
            f"abs_path: {abs_path}\n"
            f"exists: {os.path.exists(abs_path)}\n"
            f"is_file: {os.path.isfile(abs_path)}\n"
            f"error: {repr(e)}\n"
        )
        return Response(debug, mimetype="text/plain; charset=utf-8"), 500

    return Response(data, mimetype="text/plain; charset=utf-8")

if __name__ == "__main__":
    # Только локально. Не запускать в сети.
    app.run(host="0.0.0.0", port=1080, debug=False)
