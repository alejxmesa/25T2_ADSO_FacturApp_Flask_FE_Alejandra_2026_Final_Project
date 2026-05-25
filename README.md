═══════════════════════════════════════════════════════════════════
  FACTURAPP - SISTEMA DE FACTURACIÓN
  Proyecto Final - Interfaz Gráfica con Flask y MySQL
═══════════════════════════════════════════════════════════════════

📋 REQUISITOS PREVIOS
─────────────────────────────────────────────────────────────────
1. Python 3.8 o superior (descargar de https://www.python.org)
2. XAMPP (descargar de https://www.apachefriends.org)
3. Navegador web (Chrome, Edge, Firefox)


═══════════════════════════════════════════════════════════════════
🔧 PASO 1: INSTALAR XAMPP Y PRENDER MySQL
═══════════════════════════════════════════════════════════════════

1. Descargá e instalá XAMPP
2. Abrí el panel de control de XAMPP
3. Dale clic en "Start" a:
   - Apache
   - MySQL
4. Verificá que ambos estén en VERDE


═══════════════════════════════════════════════════════════════════
🔧 PASO 2: CREAR LA BASE DE DATOS
═══════════════════════════════════════════════════════════════════

1. Abrí tu navegador
2. Andá a: http://localhost/phpmyadmin
3. En el panel izquierdo, clic en "Nueva" (para crear base de datos)
4. Escribí el nombre: trabajo_final_facturacion
5. Clic en "Crear"
6. Clic en la base de datos creada (trabajo_final_facturacion)
7. Clic en la pestaña "Importar"
8. Clic en "Seleccionar archivo"
9. Buscá el archivo: Trabajo_Final_Facturacion.sql
10. Bajá hasta abajo y clic en "Importar"

✅ Listo, la base de datos está creada con todas las tablas.


═══════════════════════════════════════════════════════════════════
🔧 PASO 3: INSTALAR DEPENDENCIAS DE PYTHON
═══════════════════════════════════════════════════════════════════

1. Abrí la terminal (CMD o PowerShell)
2. Navegá hasta la carpeta del proyecto:
   cd 25T2_ADSO_FacturApp_Flask_FE
   cd src

3. Instalá la librería de MySQL:
   pip install mysql-connector-python==8.0.33

4. Si te pide actualizar pip, podés hacerlo:
   python -m pip install --upgrade pip


═══════════════════════════════════════════════════════════════════
🔧 PASO 4: CORRER LA APLICACIÓN
═══════════════════════════════════════════════════════════════════

1. En la terminal, asegurate de estar en la carpeta src:
   cd src

2. Ejecutá:
   python app.py

3. Si todo sale bien, vas a ver:
   * Serving Flask app 'app'
   * Debug mode: on
   * Running on http://127.0.0.1:5000

4. NO CIERRES la terminal mientras usás la aplicación


═══════════════════════════════════════════════════════════════════
🌐 PASO 5: ABRIR EN EL NAVEGADOR
═══════════════════════════════════════════════════════════════════

1. Abrí Chrome, Edge o Firefox
2. Andá a: http://127.0.0.1:5000
3. ¡Listo! La aplicación debería cargar


═══════════════════════════════════════════════════════════════════
📁 ESTRUCTURA DEL PROYECTO
═══════════════════════════════════════════════════════════════════

25T2_ADSO_FacturApp_Flask_FE/
├── src/
│   ├── app.py              ← Archivo principal de Flask
│   └── templates/          ← Todas las páginas HTML
│       ├── base.html       ← Template base con navbar
│       ├── index.html      ← Página principal (Dashboard)
│       ├── ListaClientes.html
│       ├── NuevoCliente.html
│       ├── EditarCliente.html
│       ├── ListaProductos.html
│       ├── NuevoProducto.html
│       ├── ListaVendedores.html
│       ├── NuevoVendedor.html
│       ├── ListaFacturas.html
│       ├── NuevaFactura.html
│       ├── DetalleFactura.html
│       ├── ResumenMensual.html
│       ├── ListaCategorias.html
│       └── NuevaCategoria.html
├── Trabajo_Final_Facturacion.sql  ← Script de base de datos
└── README.txt              ← Este archivo


═══════════════════════════════════════════════════════════════════
⚠️ SOLUCIÓN DE PROBLEMAS
═══════════════════════════════════════════════════════════════════

PROBLEMA: "No se puede acceder al sitio" o "ERR_CONNECTION_REFUSED"
SOLUCIÓN: Verificá que:
  - XAMPP esté prendido (Apache y MySQL en verde)
  - La terminal con "python app.py" esté abierta
  - Estés en la URL correcta: http://127.0.0.1:5000

PROBLEMA: "Error conectando a MySQL"
SOLUCIÓN: Verificá que:
  - La base de datos "trabajo_final_facturacion" exista en phpMyAdmin
  - XAMPP MySQL esté corriendo
  - La contraseña de root esté vacía (por defecto en XAMPP)

PROBLEMA: "ModuleNotFoundError: No module named 'mysql'"
SOLUCIÓN: Instalá la librería:
  pip install mysql-connector-python==8.0.33

PROBLEMA: "No such file or directory: app.py"
SOLUCIÓN: Verificá que estés en la carpeta correcta:
  cd 25T2_ADSO_FacturApp_Flask_FE
  cd src


═══════════════════════════════════════════════════════════════════
🎯 FUNCIONALIDADES DE LA APLICACIÓN
═══════════════════════════════════════════════════════════════════

✅ Dashboard con estadísticas en tiempo real
✅ Gestión de Clientes (Crear, Leer, Actualizar, Eliminar)
✅ Gestión de Productos con control de stock
✅ Gestión de Vendedores
✅ Gestión de Categorías/Etiquetas para productos
✅ Creación de Facturas con múltiples productos
✅ Detalle completo de facturas con totales
✅ Resumen mensual de facturación con gráfico
✅ Diseño responsive (funciona en celular y computadora)


═══════════════════════════════════════════════════════════════════
👨‍💻 DESARROLLADO POR
═══════════════════════════════════════════════════════════════════

Equipo: FacturApp Team
Proyecto Final de Facturación - ADSO


═══════════════════════════════════════════════════════════════════
📞 CONTACTO Y SOPORTE
═══════════════════════════════════════════════════════════════════

Si tenés problemas para instalar:
1. Verificá que XAMPP esté en verde
2. Verificá que la base de datos esté importada
3. Verificá que estés en la carpeta src al correr python app.py

═══════════════════════════════════════════════════════════════════
