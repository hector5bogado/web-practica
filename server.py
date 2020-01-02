from flask import Flask
from flask import request
from flask import make_response
from flask import url_for
from flask import jsonify
from flask import redirect
import sqlite3

app = Flask(__name__)
#----------------------------------------------------------------------------
#       ---------- Acá solo voy a poner las funsiones ----------
#----------------------------------------------------------------------------
#Verificar si el nombre ya existe en el sistema
def existeCodigo(codigo_web):
    conn = sqlite3.connect('prac.db')
    c = conn.cursor()
    codigo_web = (codigo_web,)
    c.execute('SELECT * FROM fichero WHERE codigo=?', codigo_web)
    respuesta = c.fetchone()
    c.close()
    conn.close()
    if respuesta:
        return True
    else:
        return False

def existeAutos(codigo_autos):
    conn = sqlite3.connect('prac.db')
    c = conn.cursor()
    codigo_autos = (codigo_autos,)     # fijarme aca.
    c.execute('SELECT * FROM autos WHERE id=?', codigo_autos)
    respuesta = c.fetchone()
    c.close()
    conn.close()
    if respuesta:
        return True
    else:
        return False

#------------------------------------------------------------------------------
#           ---------- Hasta acá las funsiones ---------- 
#------------------------------------------------------------------------------

@app.route("/web",methods= ['POST','GET','DELETE'])
def algo():
    url_for('static', filename='web_uno.html')
    url_for('static', filename='bootstrap.css')
    url_for('static', filename='jquery.js')

    # Poner aca para que se conecte con la base de datos para cargar el nombre del cliente.
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        marca = request.form['marca']

        if existeCodigo(codigo):
            #ACTUALIZAR DATOS DEL CLIENTE.
            conn = sqlite3.connect('prac.db')
            c = conn.cursor()
            c.execute("""UPDATE fichero SET nombre='%s',marca='%s' WHERE codigo='%s'""" % (nombre,marca,codigo))
            conn.commit()
        else:    
            #GUARDAR NUEVO CLIENTE.
            conn = sqlite3.connect('prac.db')
            c = conn.cursor()
            c.execute("""INSERT INTO fichero VALUES (%s,'%s','%s')""" % (codigo, nombre,marca))
            conn.commit()
        c.close()
        conn.close()
        return redirect("http://127.0.0.1:3000/static/web_uno.html", code=302)

    # Para el listado 
    if request.method == 'GET':
        conn = sqlite3.connect('prac.db')
        c = conn.cursor()
        
        if 'codigo' in request.args:
            codigo = request.args.get('codigo')
            c.execute("""SELECT * FROM fichero WHERE codigo = %s""" % codigo)
        elif 'marca' in request.args:
            marca = request.args.get('marca')
            c.execute("""SELECT * FROM fichero WHERE marca = %s""" % marca)
        else:
            c.execute("""SELECT * FROM fichero""")

        libros = c.fetchall()
        respuesta = []
        for libro in libros:
            # libro es un diccionario en python
            libro = {'codigo':libro[0],
                    'nombre':libro[1],
                    'marca':libro[2]}
            respuesta.append(libro)
        return jsonify({"data":respuesta})
    
    # Esta parte borra de la base los datos elegidos 
    if request.method == 'DELETE':
        codigo = request.args.get('codigo')
        conn = sqlite3.connect('prac.db')
        c = conn.cursor()
        c.execute("""DELETE FROM fichero WHERE codigo = %s""" % codigo)
        conn.commit()
        c.close()
        conn.close()
        return make_response(jsonify({'respuesta':'ok'}), 200)

#-------------------------------------------------------------------------------
@app.route("/autos", methods=['GET','POST','DELETE'])
def guardarAutos(): # fijarme aca
    url_for('static', filename='web_dos.html')
    url_for('static', filename='bootstrap.css')
    url_for('static', filename='jquery.js')

    if request.method == 'POST':
        id = request.form['id']
        marca = request.form['marca']

        if existeAutos(id):
            #ACTUALIZAR DATOS DE AUTOS
            conn = sqlite3.connect('prac.db')
            c = conn.cursor()                       # este le agregue con nandy
            c.execute("""UPDATE autos SET marca='%s' WHERE id='%s'""" % (marca,id))
            conn.commit()
        else:    
            #GUARDAR NUEVO AUTO
            conn = sqlite3.connect('prac.db')
            c = conn.cursor()
            c.execute("""INSERT INTO autos VALUES (%s,'%s')""" % (id,marca))
            conn.commit()
        c.close()
        conn.close()

        return redirect("http://127.0.0.1:3000/static/web_dos.html", code=302)

    if request.method == 'GET':
        conn = sqlite3.connect('prac.db')
        c = conn.cursor()
        
        if 'id' in request.args:
            id = request.args.get('id')
            c.execute("""SELECT * FROM autos WHERE id = %s""" % id)
        elif 'marca' in request.args:
            marca = request.args.get('marca')
            c.execute("""SELECT * FROM autos WHERE marca = %s""" % marca)
        else:
            c.execute("""SELECT * FROM autos""")

        autores = c.fetchall()

        respuesta = []
        for autor in autores:
            # autor es un diccionario en python
            autor = {'id':autor[0],
                    'marca':autor[1]}
            respuesta.append(autor)
        return jsonify({"data":respuesta})

    # Borra un libro del sistema
    if request.method == 'DELETE':
        id = request.args.get('id')
        conn = sqlite3.connect('prac.db')
        c = conn.cursor()
        c.execute("""DELETE FROM autos WHERE id = %s""" % id)
        conn.commit()
        c.close()
        conn.close()
        return make_response(jsonify({'respuesta':'ok'}), 200)

if __name__ == "__main__":
    app.run(debug=True, port=3000)