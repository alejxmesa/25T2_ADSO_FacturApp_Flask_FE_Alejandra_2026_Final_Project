from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import traceback

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# ───────────────────────────────────────────────
# CONFIGURACIÓN DE BASE DE DATOS
# ───────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'trabajo_final_facturacion'
}

def get_db_connection():
    """Crea y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexión a MySQL exitosa!")
        return conn
    except Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        traceback.print_exc()
        return None

# ═══════════════════════════════════════════════
# RUTAS PRINCIPALES
# ═══════════════════════════════════════════════

@app.route("/")
def index():
    print("🌐 Accediendo a index...")
    conn = get_db_connection()
    stats = {}
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS total FROM Clientes")
            stats['clientes'] = cursor.fetchone()['total']
            cursor.execute("SELECT COUNT(*) AS total FROM Productos")
            stats['productos'] = cursor.fetchone()['total']
            cursor.execute("SELECT COUNT(*) AS total FROM Vendedores")
            stats['vendedores'] = cursor.fetchone()['total']
            cursor.execute("SELECT COUNT(*) AS total FROM Facturas")
            stats['facturas'] = cursor.fetchone()['total']
            cursor.execute("SELECT * FROM Resumen_Mensual ORDER BY anio DESC, mes DESC LIMIT 6")
            stats['resumen'] = cursor.fetchall()
            cursor.close()
            conn.close()
            print("✅ Datos cargados correctamente")
        except Exception as e:
            print(f"❌ Error en consultas: {e}")
            traceback.print_exc()
    else:
        print("⚠️ No se pudo conectar a la base de datos")
    return render_template("index.html", stats=stats)

# ═══════════════════════════════════════════════
# CLIENTES
# ═══════════════════════════════════════════════

@app.route("/lista-clientes")
def listaClientes():
    conn = get_db_connection()
    clientes = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clientes ORDER BY id DESC")
            clientes = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en listaClientes: {e}")
    return render_template("ListaClientes.html", clientes=clientes)

@app.route("/nuevo-cliente", methods=["GET", "POST"])
def nuevoCliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Clientes (nombre, email, telefono) VALUES (%s, %s, %s)",
                    (nombre, email, telefono)
                )
                conn.commit()
                cursor.close()
                conn.close()
                flash("Cliente registrado exitosamente", "success")
                return redirect(url_for("listaClientes"))
            except Exception as e:
                print(f"❌ Error insertando cliente: {e}")
                flash(f"Error: {e}", "danger")
    return render_template("NuevoCliente.html")

@app.route("/editar-cliente/<int:id>", methods=["GET", "POST"])
def editarCliente(id):
    conn = get_db_connection()
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Clientes SET nombre=%s, email=%s, telefono=%s WHERE id=%s",
                    (nombre, email, telefono, id)
                )
                conn.commit()
                cursor.close()
                conn.close()
                flash("Cliente actualizado", "success")
                return redirect(url_for("listaClientes"))
            except Exception as e:
                print(f"❌ Error actualizando cliente: {e}")

    cliente = None
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clientes WHERE id = %s", (id,))
            cliente = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error obteniendo cliente: {e}")
    return render_template("EditarCliente.html", cliente=cliente)

@app.route("/eliminar-cliente/<int:id>")
def eliminarCliente(id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Clientes WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Cliente eliminado", "danger")
        except Exception as e:
            print(f"❌ Error eliminando cliente: {e}")
    return redirect(url_for("listaClientes"))

# ═══════════════════════════════════════════════
# PRODUCTOS
# ═══════════════════════════════════════════════

@app.route("/lista-productos")
def listaProductos():
    conn = get_db_connection()
    productos = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, c.nombre AS categoria_nombre 
                FROM Productos p 
                JOIN Categorias c ON p.categoria_id = c.id 
                ORDER BY p.id DESC
            """)
            productos = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en listaProductos: {e}")
    return render_template("ListaProductos.html", productos=productos)

@app.route("/nuevo-producto", methods=["GET", "POST"])
def nuevoProducto():
    conn = get_db_connection()
    categorias = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Categorias")
            categorias = cursor.fetchall()

            if request.method == "POST":
                descripcion = request.form["descripcion"]
                valor_unitario = request.form["valor_unitario"]
                stock = request.form["stock"]
                categoria_id = request.form["categoria_id"]

                cursor.execute(
                    "INSERT INTO Productos (descripcion, valor_unitario, stock, categoria_id) VALUES (%s, %s, %s, %s)",
                    (descripcion, valor_unitario, stock, categoria_id)
                )
                conn.commit()
                cursor.close()
                conn.close()
                flash("Producto registrado exitosamente", "success")
                return redirect(url_for("listaProductos"))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en nuevoProducto: {e}")
    return render_template("NuevoProducto.html", categorias=categorias)

# ═══════════════════════════════════════════════
# VENDEDORES
# ═══════════════════════════════════════════════

@app.route("/lista-vendedores")
def listaVendedores():
    conn = get_db_connection()
    vendedores = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Vendedores ORDER BY id DESC")
            vendedores = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en listaVendedores: {e}")
    return render_template("ListaVendedores.html", vendedores=vendedores)

@app.route("/nuevo-vendedor", methods=["GET", "POST"])
def nuevoVendedor():
    if request.method == "POST":
        nombre = request.form["nombre"]

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Vendedores (nombre) VALUES (%s)", (nombre,))
                conn.commit()
                cursor.close()
                conn.close()
                flash("Vendedor registrado exitosamente", "success")
                return redirect(url_for("listaVendedores"))
            except Exception as e:
                print(f"❌ Error insertando vendedor: {e}")
    return render_template("NuevoVendedor.html")


# ═══════════════════════════════════════════════
# CATEGORÍAS
# ═══════════════════════════════════════════════

@app.route("/lista-categorias")
def listaCategorias():
    conn = get_db_connection()
    categorias = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Categorias ORDER BY id DESC")
            categorias = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en listaCategorias: {e}")
    return render_template("ListaCategorias.html", categorias=categorias)

@app.route("/nueva-categoria", methods=["GET", "POST"])
def nuevaCategoria():
    if request.method == "POST":
        nombre = request.form["nombre"]
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Categorias (nombre) VALUES (%s)", (nombre,))
                conn.commit()
                cursor.close()
                conn.close()
                flash("Categoría registrada exitosamente", "success")
                return redirect(url_for("listaCategorias"))
            except Exception as e:
                print(f"❌ Error insertando categoría: {e}")
                flash(f"Error: {e}", "danger")
    return render_template("NuevaCategoria.html")



# ═══════════════════════════════════════════════
# FACTURAS
# ═══════════════════════════════════════════════

@app.route("/lista-facturas")
def listaFacturas():
    conn = get_db_connection()
    facturas = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.id, f.fecha, c.nombre AS cliente, v.nombre AS vendedor, f.anio,
                       SUM(fp.cantidad * fp.precio_unitario) AS total
                FROM Facturas f
                JOIN Clientes c ON f.cliente_id = c.id
                JOIN Vendedores v ON f.vendedor_id = v.id
                LEFT JOIN Factura_Productos fp ON f.id = fp.factura_id
                GROUP BY f.id
                ORDER BY f.id DESC
            """)
            facturas = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en listaFacturas: {e}")
    return render_template("ListaFacturas.html", facturas=facturas)

@app.route("/nueva-factura", methods=["GET", "POST"])
def nuevaFactura():
    conn = get_db_connection()
    clientes = []
    vendedores = []
    productos = []
    anios = []

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clientes")
            clientes = cursor.fetchall()
            cursor.execute("SELECT * FROM Vendedores")
            vendedores = cursor.fetchall()
            cursor.execute("SELECT * FROM Productos WHERE stock > 0")
            productos = cursor.fetchall()
            cursor.execute("SELECT * FROM Anios")
            anios = cursor.fetchall()

            if request.method == "POST":
                fecha = request.form["fecha"]
                cliente_id = request.form["cliente_id"]
                vendedor_id = request.form["vendedor_id"]
                anio = request.form["anio"]
                productos_seleccionados = request.form.getlist("producto_id[]")
                cantidades = request.form.getlist("cantidad[]")

                cursor.execute(
                    "INSERT INTO Facturas (fecha, cliente_id, vendedor_id, anio) VALUES (%s, %s, %s, %s)",
                    (fecha, cliente_id, vendedor_id, anio)
                )
                factura_id = cursor.lastrowid

                for prod_id, cant in zip(productos_seleccionados, cantidades):
                    if int(cant) > 0:
                        cursor.execute("SELECT valor_unitario FROM Productos WHERE id = %s", (prod_id,))
                        precio = cursor.fetchone()["valor_unitario"]
                        cursor.execute(
                            "INSERT INTO Factura_Productos (factura_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                            (factura_id, prod_id, cant, precio)
                        )
                        cursor.execute(
                            "UPDATE Productos SET stock = stock - %s WHERE id = %s",
                            (cant, prod_id)
                        )

                conn.commit()
                cursor.close()
                conn.close()
                flash("Factura creada exitosamente", "success")
                return redirect(url_for("listaFacturas"))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en nuevaFactura: {e}")
            traceback.print_exc()
    return render_template("NuevaFactura.html", clientes=clientes, vendedores=vendedores, 
                           productos=productos, anios=anios)

@app.route("/detalle-factura/<int:id>")
def detalleFactura(id):
    conn = get_db_connection()
    factura = None
    productos = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.*, c.nombre AS cliente, c.email, c.telefono, v.nombre AS vendedor
                FROM Facturas f
                JOIN Clientes c ON f.cliente_id = c.id
                JOIN Vendedores v ON f.vendedor_id = v.id
                WHERE f.id = %s
            """, (id,))
            factura = cursor.fetchone()

            cursor.execute("""
                SELECT fp.*, p.descripcion AS producto_nombre
                FROM Factura_Productos fp
                JOIN Productos p ON fp.producto_id = p.id
                WHERE fp.factura_id = %s
            """, (id,))
            productos = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en detalleFactura: {e}")
    return render_template("DetalleFactura.html", factura=factura, productos=productos)

@app.route("/resumen-mensual")
def resumenMensual():
    conn = get_db_connection()
    resumen = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Resumen_Mensual ORDER BY anio DESC, mes DESC")
            resumen = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en resumenMensual: {e}")
    return render_template("ResumenMensual.html", resumen=resumen)

# ═══════════════════════════════════════════════
# INICIAR SERVIDOR
# ═══════════════════════════════════════════════

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📊 Probando conexión a MySQL...")
    test_conn = get_db_connection()
    if test_conn:
        test_conn.close()
        print("✅ Todo listo! Abrí http://127.0.0.1:5000 en tu navegador")
    else:
        print("⚠️ No se pudo conectar a MySQL, pero el servidor va a iniciar igual")
    app.run(debug=True)