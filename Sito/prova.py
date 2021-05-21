import sqlite3, requests, jinja2
from flask import Flask, app, json,render_template, redirect, request, jsonify


app = Flask(__name__)

#0: id
#1: Titolo
#2: Descr
#3: Regista
#4: Località
#5: Valutazione
#6: NumValut
#7: Data
#8: Path
email="tommaso.genovese@itiscuneo.eu"
pwd="5f4dcc3b5aa765d61d8327deb882cf99"

with sqlite3.connect("web.db") as conn:
    cur=conn.cursor()
    query1=f"SELECT id FROM clienti WHERE Email = '{email}' AND Pwd = '{pwd}'"
    cur.execute(query1)
    conn.commit()
    id=cur.fetchone()
    print(id[0])


    