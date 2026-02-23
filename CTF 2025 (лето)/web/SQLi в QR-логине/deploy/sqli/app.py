from flask import Flask, request, session, redirect, url_for, render_template_string
import sqlite3
from pyzbar import pyzbar
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = 'KrXo7YaA3VAb5g>sehK<mQfrPDASVvQJQV++<oT5ynV3U?dNcb'

def get_db():
    """Возвращает новое соединение с SQLite"""
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'JH3t5vpj')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'pass123')")

    conn.commit()
    return conn, c

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('qr_login'))

    return render_template_string('''
        <div class="container">
            <h1>Добро пожаловать, {{ session['user'] }}!</h1>
            <a href="/flag" class="btn">Мой профиль</a><br>
            <a href="/logout" class="btn">Выйти</a>
        </div>
    ''')

@app.route('/qr-login', methods=['GET', 'POST'])
def qr_login():
    result = ""
    if request.method == 'POST':
        file = request.files.get('qrcode')
        if not file:
            return "Необходимо выбрать файл", 400

        try:
            img = Image.open(file.stream)
            decoded = pyzbar.decode(img)

            if decoded:
                data = decoded[0].data.decode('utf-8').strip()
                parts = data.split(':', 1)

                if len(parts) != 2:
                    return "Формат QR-кода должен быть: username:password"

                username, password = parts

                # Получаем новое соединение и курсор
                conn, c = get_db()

                # Очень простая и уязвимая реализация
                c.execute(f"SELECT * FROM users WHERE username = '{username}'")
                user = c.fetchone()

                if user and user[2] == password:
                    session['user'] = username
                    return f'''<p>Вы вошли как {username}</p>
                    <a href="/flag">get_flag</a>'''
                elif user:
                    return "<p>Неправильный пароль</p>"
                else:
                    return "<p>Пользователь не найден</p>"

            else:
                return "<p>Неверный QR код</p>"

        except Exception as e:
            return f"<p>Ошибка: {e}</p>"

    return render_template_string('''
        <div class="container">
            <h2>QR Code Login</h2>
            <p>Загрузите QR-код, содержащий логин и пароль в формате: <code>username:password</code></p>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="qrcode" required><br><br>
                <input type="submit" value="Войти через QR код" class="btn">
            </form>

            <hr>
            <p><strong>Пример:</strong> Сгенерируйте QR-код со следующим текстом: <code>user:pass123</code></p>
            <p>Загрузите его сюда, чтобы войти как пользователь <code>user</code>.</p>
            <!-- А если вы хитрый участник — попробуйте обойти защиту и войти как <code>admin</code> -->
        </div>
    ''')

@app.route('/flag')
def get_flag():
    if 'user' not in session or session['user'] != 'admin':
        return "Доступ запрещён", 403
    return "FECTF{sql_injection_from_qr_code_1337}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('qr_login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)