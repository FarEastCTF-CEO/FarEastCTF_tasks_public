#!/usr/bin/env python3
import os
import time
import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'password')
DB_NAME = os.environ.get('DB_NAME', 'bank_db')

_conn = None

def get_conn():
    """Create (or reuse) a DB connection. Retries help when DB container isn't ready yet."""
    global _conn
    if _conn is not None:
        try:
            _conn.ping(reconnect=True)
            return _conn
        except Exception:
            _conn = None

    last_err = None
    for _ in range(30):
        try:
            _conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            return _conn
        except Exception as e:
            last_err = e
            time.sleep(1)
    raise RuntimeError(f"DB connection failed: {last_err}")


def get_cryptonames():
    con = get_conn()
    with con.cursor() as cur:
        cur.execute('SELECT crypto_name FROM cryptocurrency;')
        return cur.fetchall()


@app.route('/')
def index():
    return render_template('index.html', cryptonames=get_cryptonames())


@app.route('/check_crypto', methods=['POST'])
def check_crypto():
    crypto = request.form.get('cryptoname', '')
    if crypto == '':
        return render_template('index.html', cryptonames=get_cryptonames(), error=True,
                               message='An empty argument was sent')

    # Intentionally vulnerable SQL query (CTF)
    query = "SELECT crypto_price FROM cryptocurrency WHERE crypto_name LIKE '" + crypto + "';"

    con = get_conn()
    try:
        with con.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    except Exception:
        return render_template('index.html', cryptonames=get_cryptonames(), error=True,
                               message='Sorry, unexpected server error')

    return render_template('index.html', cryptonames=get_cryptonames(), crypto_price=rows, crypto=crypto)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
