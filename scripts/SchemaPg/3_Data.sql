
-- usuarios
INSERT INTO sy_user (username,email,name,passwd) VALUES
('admin','admin@gmail.com','Administrador','admin'),
('usuario01','usuario01@gmail.com','Usuario 01','admin'),
('usuario02','usuario02@gmail.com','Usuario 02','admin');


-- roles
INSERT INTO sy_role(name) VALUES 
('Administrador'),
('Supervisor'),
('Operador'),
('Usuario');

-- usuarios por rol
INSERT INTO sy_user_role(sy_user_id, sy_role_id) VALUES 
((SELECT _id FROM sy_user WHERE username = 'admin'),(SELECT _id FROM sy_role WHERE name = 'Administrador')),
((SELECT _id FROM sy_user WHERE username = 'usuario01'),(SELECT _id FROM sy_role WHERE name = 'Supervisor')),
((SELECT _id FROM sy_user WHERE username = 'usuario02'),(SELECT _id FROM sy_role WHERE name = 'Operador'));

-- articulos
INSERT INTO art (name, code) VALUES
('BANDERAS', '0000010'),
('BLUE RAY SONY', '0000022'),
('CAJA DE SONODO WBTV', '0000051'),
('CENEFAS MOVIE CITY', '0000090'),
('MEGAFONOS', '0000154'),
('TRIPODE DE ANTENA', '0000204');

-- almacenes
INSERT INTO whs (name) VALUES
('SUR'),
('NORTE'),
('CENTRAL');

-- motivos
INSERT INTO rsn (name,sgn) VALUES
('Carga Inicial', 1),
('Compra', 1),
('Devolución', 1),
('Salida', -1),
('Devolución', -1);