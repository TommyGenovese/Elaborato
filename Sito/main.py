from flask import Flask, render_template, redirect, url_for, request
import sqlite3, hashlib, mysql.connector
#add log
app = Flask(__name__)

@app.route("/", methods=['GET'])             #http://127.0.0.1:5000/
def main():
    print("Main")
    return render_template("registrazione.html")

@app.route('/', methods=['POST'])
def registration():
    #pagina di registrazione del biglietto
    email = request.form['email']
    pwd = hashlib.md5(request.form["pwd"].encode()).hexdigest()
    
    with sqlite3.connect("web.db") as conn:
        cur= conn.cursor()
        print("Select")
        cur.execute(f"SELECT * FROM reg WHERE Email = '{email}' AND pwd = '{pwd}'")
        data = cur.fetchone()
        if data is None:
            query=f"INSERT INTO reg(Email, pwd) VALUES ('{email}', '{pwd}')"
            cur.execute(query)
            conn.commit()
            print(cur.rowcount, "record inseriti")
            saluto= "BENVENUTO, "
            #ottieni films
            return render_template('seat.html',Saluto=saluto, nome=email)
        else:
            saluto="BENTORNATO, "
            return render_template('seat.html',Saluto=saluto, nome=email)

@app.route("/seat", methods=['GET'])
def seatt():
    print("Flight")
    return render_template("Seat.html")

@app.route('/seat', methods=['POST'])
def seat():
    #pagina di registrazione del biglietto
    Volo = request.form['NumVolo']
    Posto = request.form['NumPosto']
    Dest = request.form['Destinazione']
    print("seat aquired")
    
    with sqlite3.connect("web.db") as conn:
        cur= conn.cursor()
        print("Select")
        cur.execute(f"SELECT * FROM reg WHERE Flight = {Volo} AND Seat = {Posto}")
        data = cur.fetchone()
        if data is None:
            query=f"INSERT INTO reg(Flight, Seat, destin) VALUES ({Volo}, {Posto}, '{Dest}')"
            cur.execute(query)
            conn.commit()
            print(cur.rowcount, "record inseriti")

            #ottieni films
            return render_template('filmChose.html', films=db2dict(cur))
        else:
            return f"Il posto {Posto}"

def db2dict(cur):
    #0: id
    #1: Titolo
    #2: Descr
    #3: Regista
    #4: Valutazione
    #5: NumValut
    #6: Data
    films={}
    cur.execute("SELECT COUNT(*) FROM Film")
    data = cur.fetchone()
    for i in range(data[0]):
        film=cur.execute(f"SELECT * FROM Film WHERE id ={i+1}").fetchone()
        films[i]=film
    return films
        

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)