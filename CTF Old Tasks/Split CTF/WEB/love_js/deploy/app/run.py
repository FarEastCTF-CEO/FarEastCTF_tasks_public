import os
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

@app.route('/')
def run_baby_run():
    return render_template('index.html')

@app.route('/<ident>')
def flag(ident: str):
    if ident == 'H_o_B_W_0_K_C_n':
        return render_template('H_o_B_W_0_K_C_n.html')
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '80'))
    app.run(host='0.0.0.0', port=port)
