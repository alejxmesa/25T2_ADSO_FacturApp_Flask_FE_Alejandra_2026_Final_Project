USE trabajo_final_facturacion;
CREATE TABLE Categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(300) NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    categoria_id INT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(id)
);

CREATE TABLE Clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20)
);

CREATE TABLE Vendedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL
);

CREATE TABLE Anios (
    anio INT PRIMARY KEY
);

CREATE TABLE Facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    cliente_id INT NOT NULL,
    vendedor_id INT NOT NULL,
    anio INT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
    FOREIGN KEY (vendedor_id) REFERENCES Vendedores(id),
    FOREIGN KEY (anio) REFERENCES Anios(anio)
);

CREATE TABLE Factura_Productos (
    factura_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (factura_id, producto_id),
    FOREIGN KEY (factura_id) REFERENCES Facturas(id),
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);

CREATE TABLE Resumen_Mensual (
    anio INT NOT NULL,
    mes INT NOT NULL,
    cantidad_facturas INT NOT NULL,
    PRIMARY KEY (anio, mes),
    FOREIGN KEY (anio) REFERENCES Anios(anio)
);
-- 2. Esto es el Trigger PARA AUTOMATIZAR LA CANTIDAD DE FACTURAS QUE TIENES HECHAS EN EL MES EN CUESTION
-- PARA USAR ESTE TRIGER ABAJO DEL TODO DEJO UN COMANDO PARA QUE APAREZCA LA TABLA FIRMADO; Alejandra.
DELIMITER $$

CREATE TRIGGER actualizar_resumen_mensual
AFTER INSERT ON Facturas
FOR EACH ROW
BEGIN
    INSERT INTO Resumen_Mensual (anio, mes, cantidad_facturas)
    VALUES (
        NEW.anio,
        MONTH(NEW.fecha),
        1
    )
    ON DUPLICATE KEY UPDATE
        cantidad_facturas = cantidad_facturas + 1;
END$$

DELIMITER ;


-- 3. INSERTS DE PRUEBA SOLO INSERTAR SI NO TIENES LOS DATOS EN TU LOCAL HOST Y SI LO INSERTAS Y TE SALE ERROR
-- NO PASA NADA ES POR QUE YA ESTA REGISTRADO Y NO LE DAS MAS: Firmado Alejandra.
INSERT INTO Categorias (nombre) VALUES ('verduras');
INSERT INTO Productos (descripcion, valor_unitario, stock, categoria_id)
VALUES ('tomates', 50.00, 10, 1);
INSERT INTO Clientes (nombre, email, telefono)
VALUES ('Juan Pérez', 'juan@email.com', '600123123');
INSERT INTO Vendedores (nombre)
VALUES ('Ana López');
INSERT INTO Anios (anio)
VALUES (2026);
INSERT INTO Factura_Productos (factura_id, producto_id, cantidad, precio_unitario)
VALUES (1, 1, 2, 50.00);
INSERT INTO Facturas (fecha, cliente_id, vendedor_id, anio)
VALUES ('2026-04-10', 1, 1, 2026);

SELECT LAST_INSERT_ID();

-- COMPROBAR QUE LA TABLA DE FACTURACION FUNCIONA, SELECIONA SOLO ESTO Y DARLE AL RAYO SOLO SI YA TIENES 
-- LOS INSERTS REGISTRADOS EN TU BD, Firmado; Alejandra.
SELECT 
    f.id AS factura,
    f.fecha,
    c.nombre AS cliente,
    v.nombre AS vendedor,
    p.descripcion AS producto,
    fp.cantidad,
    fp.precio_unitario,
    (fp.cantidad * fp.precio_unitario) AS total
FROM Facturas f
JOIN Clientes c ON f.cliente_id = c.id
JOIN Vendedores v ON f.vendedor_id = v.id
JOIN Factura_Productos fp ON f.id = fp.factura_id
JOIN Productos p ON fp.producto_id = p.id;

-- PARA USAR El COMANDO DE ESTE TRIGER SELECCIONA TODO LO DE ABAJO Y DALE AL RAYO FIRMADO ALEJANDRA.

SELECT * FROM Factura_Productos;
SELECT * FROM Resumen_Mensual;
