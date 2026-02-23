#!/usr/bin/env python
import dataset
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import session
from flask import url_for
import os
import urllib.request
import datetime
import pymysql.cursors



app = Flask(__name__, static_folder='static', static_url_path='')
use_debugger=True

con = pymysql.connect(
    host='localhost',
    user='root',
    password='12323212t',
    db='bank_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
#print ("connect successful!!")

def check_sql(crypto):
    vuln = ["select", "SELECT", "union", "UNION", "from", "FROM", " ", "  "]
    vuln = []
    for v in vuln:
        if crypto.find(v) >=0:
            error = True
            message="Forbidden construct detected: '"+v+"'"
            return error, message
    return False, ''    
        
def get_criptoname():
    curr = con.cursor()
    query = 'select crypto_name from cryptocurrency;'
    try:
        curr.execute(query)
        rowss = curr.fetchall()
        message=""
        return (rowss, message)
    except:
        message="Sorry, unexpected server error"
        return (rowss, message)

@app.route('/')
def index():
    criptoname , message = get_criptoname()
    return render_template('index.html', criptoname=criptoname, message=message)



@app.route('/check_crypto', methods=['GET', 'POST'])
def check_crypto():
    crypto = request.form['cryptoname']
    if crypto =="":
        error = 'True'
        message="An empty argument was sent"
        return render_template('index.html', error=error, message=message)
    error, message = check_sql(crypto)
    if error:
        return render_template('index.html', error=error, message=message)
    cur = con.cursor()
    query = 'select crypto_price from cryptocurrency where crypto_name LIKE \'' + crypto + '\';'
    try:
        cur.execute(query)
        rows = cur.fetchall()
#        for row in rows:
#            print(row)
 
        criptoname , message = get_criptoname()
        return render_template('index.html', crypto_price=rows, crypto=crypto, criptoname=criptoname, message=message)
    except:
        error = 'True'
        message="Sorry, unexpected server error"
        return render_template('index.html', error=error, message=message)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

