#!/usr/bin/env python3
import os
import time
import pymysql.cursors
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static', static_url_path='')

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'bank_db')


def get_connection():
    """Connect to MySQL with a small retry loop (useful in docker-compose)."""
    last_err = None
    for _ in range(40):  # ~40 seconds max
        try:
            return pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                db=DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
        except Exception as e:
            last_err = e
            time.sleep(1)
    raise last_err


con = get_connection()


def check_sql(crypto: str):
    # Intentionally weak blacklist (challenge).
    vuln = ["select", "SELECT", "union", "UNION", "from", "FROM"]
    for v in vuln:
        if crypto.find(v) >= 0:
            return True, f"Forbidden construct detected: '{v}'"
    return False, ""


def get_criptoname():
    curr = con.cursor()
    query = 'select crypto_name from cryptocurrency;'
    try:
        curr.execute(query)
        rowss = curr.fetchall()
        return rowss, ""
    except Exception:
        return [], "Sorry, unexpected server error"


@app.route('/')
def index():
    criptoname, message = get_criptoname()
    return render_template('index.html', criptoname=criptoname, message=message)


@app.route('/check_crypto', methods=['POST'])
def check_crypto():
    crypto = request.form.get('cryptoname', '')
    if crypto == "":
        return render_template('index.html', error='True', message="An empty argument was sent")

    error, message = check_sql(crypto)
    if error:
        return render_template('index.html', error=error, message=message)

    cur = con.cursor()
    # Vulnerable to SQL injection (challenge).
    query = "select crypto_price from cryptocurrency where crypto_name LIKE '" + crypto + "';"

    try:
        cur.execute(query)
        rows = cur.fetchall()
        criptoname, message = get_criptoname()
        return render_template('index.html', crypto_price=rows, crypto=crypto, criptoname=criptoname, message=message)
    except Exception:
        return render_template('index.html', error='True', message="Sorry, unexpected server error")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
