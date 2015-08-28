-- sample file to test sample
-- INSERT INTO empresa (ruc, description, address, phone, email, setame, created_on)
-- VALUES ('10900417679', 'Alo 21', 'Av. Pedro Ruiz 910, La Molina, Lima', '621-2121', 'info@alo.pe', True, now());

-- INSERT INTO vehiculo (placa, marca, modelo, color, created_on)
-- VALUES ('L7J-078', 'Toyota', 'Corolla', 'Blanco', now());

-- INSERT INTO conductor (dni, nombre, licencia, created_on)
-- VALUES ('1904111652', 'Salvador Jimenez Ballesteros', 'E07818103', now());

-- INSERT INTO vehiculo_conductor (uuid, placa, dni, ruc, created_on)
-- VALUES ('c105b22c-8db3-4f79-935a-404bac3023d2', 'L7J-078','1904111652', '10900417679', True, now());
-- INSERT INTO uuid_store (uuid, created_on)
-- VALUES ('c105b22c-8db3-4f79-935a-404bac3023d2', now());

INSERT INTO sy_user (email, password, name, rol, is_active, created_on)
VALUES ('reynaldomic@gmail.com', '$pbkdf2-sha256$8684$QChFCEEIoVQKQci5l5Iyhg$THMB/xljNCkHPCkoy4ASRP8JOmEmoZHr0IKEOhBxHXc', 'Reynaldo Baquerizo', 'staff', True, now());
