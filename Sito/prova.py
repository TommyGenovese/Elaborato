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

@app.route("/")
def home():
    films={}
    with sqlite3.connect("web.db") as conn:
        cur= conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Film")
        data = cur.fetchone()
        for i in range(data[0]):
            film=cur.execute(f"SELECT * FROM Film WHERE id ={i+1}").fetchone()
            films[i]=film
            print(f"\n{films[i]}")
    return render_template("filmChose.html", films=films)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)

    