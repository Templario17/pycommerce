/*mapeo Base de datos*/

CREATE TABLE IF NOT EXISTS categoria(
	categoria_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	denominacion VARCHAR(50)
)ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS producto(
    producto_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    denominacion VARCHAR(100),
    descripcion VARCHAR(250),
    precio_lista DECIMAL(10, 2),
    precio_oferta DECIMAL(10, 2),
    sku VARCHAR(12),
    categoria INT(11),
    INDEX(categoria),
    FOREIGN KEY (categoria)
        REFERENCES categoria(categoria_id)
        ON DELETE CASCADE
)ENGINE=InnoDB;
