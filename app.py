from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app= Flask(__name__)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= '123456'
app.config['MYSQL_DB']= 'tienda'

mysql= MySQL(app)

app.secret_key= 'mysecretkey'

@app.route('/')
def principal():
    return render_template('pagina_inicial.html')

@app.route('/ver_producto')
def index():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    datos= cur.fetchall()
    return render_template('ver_producto.html', productos= datos)

@app.route('/agregar')
def productos():
    return redirect(url_for('index'))

@app.route('/agregar_producto', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombre_producto=request.form['nombre_producto']
        cantidad=request.form['cantidad']
        precio= request.form['precio']
        precio_compra=request.form['precio_compra']
        cursor= mysql.connection.cursor()
        cursor.execute('INSERT INTO productos (nombre_producto,cantidad, precio, precio_compra) VALUES (%s,%s,%s,%s)',(nombre_producto,cantidad,precio,precio_compra))
        mysql.connection.commit()
        flash('PRODUCTO AGREGADO CORRECTAMENTE')
        return render_template('agregar_producto.html')


@app.route('/editar_producto')
def editar_producto():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    datos= cur.fetchall()
    return render_template('editar_producto.html', productos= datos)

@app.route('/editar/<string:id>')
def editar(id):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE codigo_producto= %s', (id))
    data= cur.fetchall()
    print(data[0])
    return render_template('editar.html',product= data[0] )

@app.route('/update/<id>')
def update(id):
    if request.method == 'post':
        nombrep=request.form["nombre_producto"]
        cantidad=request.form["cantidad"]
        preciop=request.form["precio_compra"]
        preciov=request.form["precio"]
        cur= mysql.connection.cursor()
        cur.execute("""
            UPDATE productos SET nombre_producto = %s, 
            cantidad= %s, 
            precio_compra= %s ,
            precio= %s 
            WHERE codigo_producto= %s                   
        """, (nombrep,cantidad,preciop,preciov,id))
        
        return redirect(url_for('editar'))
    

@app.route('/eliminar_producto')
def eliminar_producto():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    datos= cur.fetchall()
    return render_template('eliminar.html', productos= datos)

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur= mysql.connection.cursor()
    cur.execute('DELETE  FROM productos where codigo_producto= {0}'.format(id))
    mysql.connection.commit()
    return render_template('eliminar.html')

if __name__ == '__main__':
    app.run(debug= True)