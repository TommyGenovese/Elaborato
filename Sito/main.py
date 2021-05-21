from flask import Flask, render_template, redirect, url_for, request
import sqlite3, hashlib, mysql.connector
from werkzeug import datastructures
#add log
app = Flask(__name__)
email = "def"
pwd = "def"
data = "def"

@app.route("/", methods=['GET'])             #http://127.0.0.1:5000/
def main():
    print("Main")
    return render_template("registrazione.html")

@app.route('/', methods=['POST'])
def registration():
    global email, pwd, data
    #pagina di registrazione del biglietto
    email = request.form['email']
    print(email)
    pwd = hashlib.md5(request.form["pwd"].encode()).hexdigest()
    
    with sqlite3.connect("web.db") as conn:
        cur= conn.cursor()
        print("Select")
        cur.execute(f"SELECT * FROM clienti WHERE Email = '{email}'")
        data = cur.fetchone()
        print(data)
        if data is None:
            query=f"INSERT INTO clienti(Email, pwd) VALUES ('{email}', '{pwd}')"
            cur.execute(query)
            conn.commit()
            print(cur.rowcount, "record inseriti")
            saluto= "BENVENUTO, "
            #ottieni films
            return render_template('ready.html',Saluto=saluto, nome=email)
        else:
            cur.execute(f"SELECT * FROM clienti WHERE email = '{email}' AND pwd='{pwd}'")
            data = cur.fetchone()
            if data is None:
                return "Password errata"
            else:
                saluto="BENTORNATO, "
                return render_template('ready.html',Saluto=saluto, nome=email)

@app.route("/seat", methods=['GET'])
def seatt():
    global data, email
    if data is None:
        saluto= "BENVENUTO, "
        return render_template('seat.html',Saluto=saluto, nome=email)
    else:
        saluto="BENTORNATO, "
        return render_template('seat.html',Saluto=saluto, nome=email)
    

@app.route('/seat', methods=['POST'])
def seat():
    global email, pwd
    #pagina di registrazione del biglietto
    Volo = request.form['NumVolo']
    Posto = request.form['NumPosto']
    Dest = request.form['Destin']
    print("seat aquired")
    
    with sqlite3.connect("web.db") as conn:
        cur= conn.cursor()
        print("Select")
        cur.execute(f"SELECT * FROM PrenSeat WHERE flight = {Volo} AND seat = {Posto}")
        data = cur.fetchone()
        if data is None:
            #cerco l'id dell'utente in modo tale da collegare i posti (>1 forse) all'utente online
            query1=f"SELECT id FROM clienti WHERE email = '{email}' AND pwd = '{pwd}'"
            print(email, pwd)
            cur.execute(query1)
            conn.commit()
            id=cur.fetchone()
            print(id[0])

            query=f"INSERT INTO PrenSeat(user, flight, seat, destin) VALUES ({id[0]},{Volo}, {Posto}, '{Dest}')"
            cur.execute(query)
            conn.commit()
            print(cur.rowcount, "record inseriti")
            #ottieni films
            return render_template('ready_film.html')
        else:
            return f"Il posto n°{Posto} nel volo n°{Volo} è già stato prenotato, non puoi effettuare modifiche"



@app.route("/film", methods=['GET'])
def fil():
    return render_template('filmChose.html', films=db2dict())
    

@app.route('/film', methods=['POST'])
def film():
    global email, pwd
    #pagina di registrazione del biglietto
    ric = request.form['Ricerca']
    print("ricerca")
    with sqlite3.connect("web.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Film WHERE Genere={ric}")
        res= cur.fetchone()
        if res is None:
            cur.execute(f"SELECT * FROM Film WHERE Regista={ric}")
            res= cur.fetchone()
            if res is None:
                return "errore di ricerca: non hai inserito il genere o il regista corretto"
            else:
                return render_template("filmChose.html", films = db2dictReg(res[0]))
        else:
            return render_template("filmChose.html", films = db2dictGen(res[0]))
    
def db2dictReg(reg):
    films={}
    with sqlite3.connect("web.db") as conn:
        cur2 = conn.cursor()
        cur2.execute(f"SELECT * FROM Film WHERE Regista = {reg}")
        data = cur2.fetchone()
        for i in range(data[0]):
            film=cur2.execute(f"SELECT * FROM Film WHERE Regista = {reg}").fetchone()
            films[i]=film
        return films

def db2dictGen(gen):
    films={}
    with sqlite3.connect("web.db") as conn:
        cur2 = conn.cursor()
        cur2.execute(f"SELECT * FROM Film WHERE Genere = {gen}")
        data = cur2.fetchone()
        for i in range(data[0]):
            film=cur2.execute(f"SELECT * FROM Film WHERE genere = {gen}").fetchone()
            films[i]=film
        return films

def db2dict():
    #0: id
    #1: Titolo
    #2: Descr
    #3: Regista
    #4: Valutazione
    #5: NumValut
    #6: Data
    films={}
    with sqlite3.connect("web.db") as conn:
        cur2 = conn.cursor()
        cur2.execute("SELECT COUNT(*) FROM Film")
        data = cur2.fetchone()
        for i in range(data[0]):
            film=cur2.execute(f"SELECT * FROM Film WHERE id ={i+1}").fetchone()
            films[i]=film
        return films
        

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)