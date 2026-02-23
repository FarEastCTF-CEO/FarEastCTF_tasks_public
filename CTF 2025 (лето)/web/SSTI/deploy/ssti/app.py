from flask import Flask, request, render_template_string
import flageeeeerrrrr

app = Flask(__name__)
app.config['SECRET_FLAG'] = "DECOY_FLAG_DO_NOT_SUBMIT"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        user_input = request.form.get('input', '')
        try:
            template = f"<h1>Привет, {{ name }}!</h1>\n<p>{user_input}</p>"
            rendered = render_template_string(template, name="Пользователь")
            return rendered
        except Exception as e:
            return f"Ошибка рендеринга: {e}"
    return render_template_string('''
        <div class="container">
            <h2>DEMO SITE</h2>
            <p><strong>Описание:</strong></p>
            <p>Мы разработали простой веб-сервис, который принимает ваш текст и выводит его на странице.</p>
            <p>Но мы не знаем, безопасен ли наш код...</p>
            <form method="post">
                <label for="input">Введите своё сообщение:</label><br>
                <input type="text" name="input" id="input" placeholder="Ваше сообщение" required><br><br>
                <input type="submit" value="Отправить" class="btn">
            </form>

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
                }
                code {
                    background-color: #eee;
                    padding: 2px 5px;
                    border-radius: 3px;
                }
            </style>
        </div>
    ''')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)