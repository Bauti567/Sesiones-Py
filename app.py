# Importando las librerias de la app
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL # Crear la localizacion de la base de datos
from datetime import datetime
from flask import send_from_directory # Permite obtener informacion de la imagen


# Inicializando la app

app = Flask(__name__) # Creando la aplicacion
app.secret_key = "JuanBautista"
# Variable de sesion

mysql = MySQL() # Crear instancia de la bae de datos



app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sitio'
mysql.init_app(app)

 
# ---------------------------------------------------------------------- #

@app.route('/') # Inicinado el template
def inicio():
    return render_template('sitio/index.html')
    # Ruta del template de inicio

# MOSTRAR IMAGENES
@app.route('/img/<imagen>')
def imagenes(imagen):

    return send_from_directory(os.path.join('templates/sitio/img'),imagen)
    

@app.route('/libros') # Agregando seccion libros
def libros():

    # Consultando info de los libros dentro de la BD
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(" SELECT * FROM `libros`")
    libros = cursor.fetchall()
    conexion.commit()



    return render_template('sitio/libros.html', libros=libros)

@app.route('/nosotros') # Agregando seccion nosotros
def nosotros():
    return render_template('sitio/nosotros.html')

# Iniciando la seccion de Admin

@app.route('/admin')
def admin_sitio():
    
    if not 'login' in session: # Si no existe el login dentro de la session no puede ingresar
        return redirect("admin/login")    
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')


# Seccion de login
@app.route('/admin/login', methods = ['POST'])
def  admin_login_post():
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    print(_usuario)
    print(_password)

    # Session de forma estática
    if _usuario == "admin" and _password == "123":
        # Variable de session 
        session["login"] = True
        session["usuario"] = "Administrador"
        
        return redirect("/admin")


    return render_template('admin/login.html')


@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear() # Limpiando las sessiones
    return redirect('/admin/login')

@app.route('/admin/libros')
def admin_libros():

    if not 'login' in session: # Si no existe el login dentro de la session no puede ingresar
        return redirect("admin/login")    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros = cursor.fetchall() # Buscar todos los datos
    conexion.commit()


    return render_template('admin/libros.html', libros = libros)
    # El libros = libros hace referencia a la variable

    
# -------- SECCION DE FILTRO DE FORMULARIO --------------------


# Enviando la información del libro
@app.route('/admin/libros/guardar', methods = ['POST'])
def admin_libros_guardar():

    if not 'login' in session: # Si no existe el login dentro de la session no puede ingresar
        return redirect("admin/login")    

    _nombre = request.form['txtNombreL']
    _url = request.form['txtURL']
    _archivo = request.files['txtImg']

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    # Retorna un string con la hora

    if _archivo.filename != "": 

        nuevoNombre = horaActual + "_" +_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)
        
        # Almacenando la imagen ingresada dentro de la ruta 


    # Ingresando los datos dentro de la BD

    sql = "INSERT INTO `libros` (`ID`, `nombre`, `Imagen`, `URL`) VALUES (NULL,%s, %s, %s);"
    datos = (_nombre, _archivo.filename, _url)
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)

    conexion.commit()

    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    
    
    if not 'login' in session: # Si no existe el login dentro de la session no puede ingresar
        return redirect("admin/login")    
    _id = request.form['txtID']



    # ------- CONSULTANDO LOS DATOS --------------------------

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `libros` WHERE id= %s", (_id))

    #----------- ELIMINANDO LOS DATOS DE LA BASE DE DATOS -----------------

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE  FROM `libros` WHERE id= %s", (_id))
    conexion.commit()

    return redirect('/admin/libros')


if __name__ == '__main__': # Cuando esté lista inicia la aplicacion
    app.run(debug = True)


