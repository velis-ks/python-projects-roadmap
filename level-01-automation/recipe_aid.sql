-- ============================================================================
-- SCRIPT Recipe_Aid (v1.0)
-- Contenido: Tablas, Datos, Vistas, Funciones, Procedures, Triggers y Eventos.
-- ============================================================================

DROP DATABASE IF EXISTS recipe_aid;
CREATE DATABASE recipe_aid CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE recipe_aid;

CREATE TABLE categories(
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	category_name VARCHAR(100)
);

CREATE TABLE recipes(
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	category_id BIGINT,
	base_portions INT,
	profit_margin DECIMAL(5,2),
	vat DECIMAL(5,2),
	is_active BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
	INDEX idx_category_id (category_id)
);

CREATE TABLE suppliers(	
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	utr VARCHAR(150) NOT NULL,
	manager VARCHAR(150) NOT NULL,
	address VARCHAR(150) NOT NULL,
	postcode VARCHAR(150) NOT NULL,
	tel VARCHAR(20),
	email VARCHAR(100) UNIQUE NOT NULL,	
	INDEX idx_email (email)
);

CREATE TABLE locations(
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	location_name VARCHAR(50)
);

CREATE TABLE ingredients(
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(250),
	location_id BIGINT,
	uom VARCHAR(20),
	waste_percentage DECIMAL(5,2),
	cost_per_kilo DECIMAL(6,2),
	supplier_id BIGINT,
	is_active BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE,
	FOREIGN KEY (supplier_id) REFERENCES suppliers (id) ON DELETE CASCADE,
	INDEX idx_location_id (location_id),
	INDEX idx_supplier_id (supplier_id)
);

CREATE TABLE recipe_ingredients(
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	recipe_id BIGINT,
	ingredient_id BIGINT,
	gross_weight_gr DECIMAL(10,2),
	FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
	FOREIGN KEY (ingredient_id) REFERENCES ingredients (id) ON DELETE CASCADE,
	INDEX idx_recipe_id (recipe_id),
	INDEX idx_ingredient_id (ingredient_id)
);


-- 1. Limpieza segura de datos (Desactivar FK temporalmente)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE recipe_ingredients;
TRUNCATE TABLE ingredients;
TRUNCATE TABLE recipes;
TRUNCATE TABLE categories;
TRUNCATE TABLE locations;  
TRUNCATE TABLE suppliers;
SET FOREIGN_KEY_CHECKS = 1;

-- 2. Insert Locations 
INSERT INTO locations (location_name) VALUES ('Dry Store'), ('Walk-in Fridge');

-- 3. Insert Supplier (Usando un proveedor local de Newquay)
INSERT INTO suppliers (name, utr, manager, address, postcode, tel, email) 
VALUES ('Cornwall Fresh Veg', 'UTR-8472', 'Tom', 'Unit 4 Treloggan Ind Est', 'TR7 2SX', '01637871234', 'orders@cornwallfresh.com');

-- 4. Insert Category
INSERT INTO categories (category_name) VALUES ('Tapas');

-- 5. Insert the Recipe
INSERT INTO recipes (name, category_id, base_portions, profit_margin, vat, is_active)
VALUES ('Classic Spanish Omelette', 1, 4, 70.00, 10.00, TRUE);

-- 6. Insert Ingredients
INSERT INTO ingredients (name, location_id, uom, waste_percentage, cost_per_kilo, supplier_id, is_active) VALUES
('Monalisa Potato', 1, 'g', 15.00, 1.20, 1, TRUE),  -- Dry Store
('Onion', 1, 'g', 10.00, 0.80, 1, TRUE),           -- Dry Store
('Egg (Unit)', 2, 'unit', 0.00, 0.25, 1, TRUE),    -- Walk-in Fridge
('EV Olive Oil', 1, 'g', 0.00, 8.50, 1, TRUE);     -- Dry Store

-- 7. Link Recipe to Ingredients
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, gross_weight_gr) VALUES
(1, 1, 1000.00), 
(1, 2, 300.00),  
(1, 3, 6.00),    
(1, 4, 200.00);
