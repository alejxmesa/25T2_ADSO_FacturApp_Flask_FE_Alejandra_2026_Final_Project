print("Hola, esto funciona!")
import mysql.connector
print("mysql.connector importado OK")

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='trabajo_final_facturacion'
    )
    print("✅ Conexión exitosa!")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Clientes")
    result = cursor.fetchone()
    print(f"Clientes: {result[0]}")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")

input("Presiona Enter para salir...")