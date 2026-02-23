from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'rxpvTjvikqXoztFp33UDLt4rYCFzCg4KFtpnQR9V5xYdSZeSfr555555'

USERS = {
    1: {'username': 'admin', 'password': 'admin'},
    2: {'username': 'user1', 'password': 'pass123'},
    5: {'username': 'user3', 'password': '!QAZ2wsx#EDC4rfv'},
    10: {'username': 'userAdm', 'password': 'IW5vdF9hZG1pbl9ub3RfYWRtaW4h'},
    20: {'username': 'userNoADM', 'password': 'Z28gdG8gL2ZsYWc='},
    53: {'username': 'SuperAdmin', 'password': 'rxpvTjvikqXoztFp33UDLt4rYCFzCg4KFtpnQR9V5xYdSZeSfr'},
}

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    for i in USERS:
        if USERS[i]['username'] == session['user']:
            id = i
    return render_template_string('''
        <div class="container">
            <h2>Добро пожаловать, {{ session['user'] }}</h2>
            <p><a href="/profile/{{ session['user_id'] }}" class="btn">Мой профиль</a></p>
            <p><a href="/logout" class="btn btn-danger">Выйти</a></p>
        </div>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                padding: 30px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h2 {
                color: #007BFF;
            }
            input[type="text"],
            input[type="password"] {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .btn {
                background-color: #007BFF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 15px;
            }
            .btn-danger {
                background-color: #dc3545;
                color: white;
            }
            p {
                margin-top: 15px;
            }
        </style>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    result = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        for user_id, user in USERS.items():
            if user['username'] == username and user['password'] == password:
                session['user'] = username
                session['user_id'] = user_id
                return redirect(url_for('index'))
        
        result = "<p style='color:red;'>Неверные логин или пароль</p>"

    return render_template_string('''
        <div class="container">
            <h2>Система дверей</h2>
            <p>Тестовый пользователь <strong>user1:pass123</strong></p>

            <form method="post">
                <label for="username">Логин:</label><br>
                <input type="text" name="username" id="username"><br><br>

                <label for="password">Пароль:</label><br>
                <input type="password" name="password" id="password"><br><br>

                <input type="submit" value="Войти" class="btn">
            </form>

            {{ result|safe }}
        </div>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                padding: 30px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h2 {
                color: #007BFF;
            }
            input[type="text"],
            input[type="password"] {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .btn {
                background-color: #007BFF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 15px;
            }
            .btn-danger {
                background-color: #dc3545;
                color: white;
            }
            p {
                margin-top: 15px;
            }
        </style>
    ''', result=result)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if user_id not in USERS:
        return "Пользователь не найден", 404
    
    user = USERS[user_id]
    
    return render_template_string('''
        <div class="container">
            <h2>Профиль пользователя</h2>
            <p><strong>Логин:</strong> {{ user['username'] }}</p>
            <p><strong>Пароль:</strong> {{ user['password'] }}</p>
            <p><a href="{{ url_for('index') }}" class="btn">Назад</a></p>
        </div>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                padding: 30px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h2 {
                color: #007BFF;
            }
            input[type="text"],
            input[type="password"] {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .btn {
                background-color: #007BFF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 15px;
            }
            .btn-danger {
                background-color: #dc3545;
                color: white;
            }
            p {
                margin-top: 15px;
            }
        </style>
    ''', user=user)

@app.route('/flag')
def flag():
    if 'user' in session and session['user'] == 'SuperAdmin':
        return "FECTF{idor_can_be_tricky}"
    return "Доступ запрещён", 403

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
