from flask import Flask, request, make_response, jsonify, render_template_string
import requests

app = Flask(__name__)
FLAG = "FECTF{ssrf_is_not_always_rce}"

@app.route('/admin')
def admin_flag():
    # Делаем флаг доступным только для внутренних запросов
    if request.remote_addr in ['127.0.0.1', 'localhost']:
        return FLAG
    else:
        return "Forbidden", 403

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "No URL provided", 400

        # Проверка, чтобы не выходить за пределы localhost
        if url.startswith("http://localhost"):
            try:
                response = requests.get(url)
                return response.text
            except Exception as e:
                result = f"<p style='color:red;'>Error fetching URL: {e}</p>"
        else:
            result = "<p style='color:red;'>URL must start with http://localhost</p>"

    return render_template_string('''
        <div class="container">
            <h2>Service</h2>
            <p><strong>Описание:</strong></p>
            <p>Я придумал как обойти политики безопасности и получать доступ без VPN. Круто же я придумал?</p>

            <form method="post">
                <label for="url">Введите URL:</label><br>
                <input type="text" name="url" id="url" placeholder="http://localhost/admin" required><br><br>
                <input type="submit" value="Получить данные" class="btn">
            </form>

            <hr>
            
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
            label {
                display: block;
                margin-top: 15px;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .btn {
                margin-top: 15px;
                background-color: #007BFF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            pre {
                background-color: #f0f0f0;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            code {
                background-color: #eee;
                padding: 2px 5px;
                border-radius: 3px;
            }
        </style>
    ''', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)