from flask import Flask, render_template, redirect, url_for, request
import sqlite3, hashlib
#add log
app = Flask(__name__)

@app.route("/")             #http://127.0.0.1:5000/
def main():
    print("Main")
    return render_template("registrazione.html")

@app.route('/', methods=['POST'])
def registration():
    #pagina di registrazione del biglietto
    Volo = request.form['NumVolo']
    Posto = request.form['NumPosto']
    Dest = request.form['Destinazione']

    
    conn = sqlite3.connect("static/web.db")
    cur= conn.cursor()
    print("Select")
    cur.execute(f"SELECT * FROM registrazioni WHERE Flight = {Volo} AND Seat = {Posto} AND destin = '{Dest}'")
    data = cur.fetchone()
    if data is None:
        query=f"INSERT INTO registrazioni(Flight, Seat, destin) VALUES ({Volo}, {Posto}, '{Dest}')"
        cur.execute(query)
        conn.commit()
        print(cur.rowcount, "record inseriti")
        return render_template('filmChose.html')
    else:
        error1 ="This seat has already been booked up"
        return error1
    return render_template('registrazione.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)