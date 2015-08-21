-- Last schema
-- ===========================================
DROP TABLE IF EXISTS vehiculo_conductor;
DROP TABLE IF EXISTS scan_event;
DROP TABLE IF EXISTS uuid_store;
DROP TABLE IF EXISTS empresa;
DROP TABLE IF EXISTS vehiculo;
DROP TABLE IF EXISTS conductor;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS dealer_user;

-- new schema
-- ===========================================
DROP TABLE IF EXISTS vehicle_driver;
DROP TABLE IF EXISTS scan_event;
DROP TABLE IF EXISTS uuid_store;
DROP TABLE IF EXISTS package_store;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS driver;
DROP TABLE IF EXISTS sy_user;

-- base user table. 
-- i could later want to add a sales type or customer or someone else, instead of creating a table I
-- prefer to use a role column.
-- After checking this http://justatheory.com/computers/databases/postgresql/enforce-set-of-values.html
-- I'll go for doing it with domains as I don't expect it to change very often and updating the constraint is more-or-less
-- straightforward.
DROP DOMAIN IF EXISTS USER_ROLE;
CREATE DOMAIN USER_ROLE AS TEXT 
CONSTRAINT VALID_USER_ROLE CHECK (
       VALUE IN ('staff', 'dealer')
);

CREATE TABLE sy_user (
       email          VARCHAR (100) PRIMARY KEY NOT NULL,
       password       VARCHAR NOT NULL,
       name           VARCHAR NOT NULL,       
       rol            USER_ROLE NOT NULL, -- notice here how i use the previously-defined domain USER_ROLE as the data-type for rol
       is_salecompany BOOLEAN NOT NULL DEFAULT FALSE,
       is_active      BOOLEAN NOT NULL DEFAULT TRUE,
       created_by   VARCHAR (100), -- the existing user who created this new user
       created_on   TIMESTAMP,     -- the date it was created
       modified_by  VARCHAR (100), -- the existing user who modified the data of this user
       modified_on  TIMESTAMP	     -- the date it was modified
);

CREATE TABLE company (
       ruc            VARCHAR (15) PRIMARY KEY NOT NULL,
       description    VARCHAR (355) NOT NULL,
       address        VARCHAR (355) NOT NULL,
       phone          VARCHAR (15)  NOT NULL,
       contact_name   VARCHAR (60),
       email          VARCHAR (355) NOT NULL,
       website        VARCHAR (150),
       is_active      BOOLEAN NOT NULL DEFAULT TRUE,
       created_by   VARCHAR (100),
       created_on   TIMESTAMP,
       modified_by  VARCHAR (100),
       modified_on  TIMESTAMP
);

CREATE TABLE vehicle (       
       plate             VARCHAR (15) PRIMARY KEY NOT NULL,
       mark              VARCHAR (45) NOT NULL,
       model             VARCHAR (45),
       color             VARCHAR (45),
       is_setame         BOOLEAN NOT NULL DEFAULT FALSE,
       is_active         BOOLEAN NOT NULL DEFAULT TRUE,
       created_by      VARCHAR (100),
       created_on      TIMESTAMP,
       modified_by     VARCHAR (100),
       modified_on     TIMESTAMP
);

CREATE TABLE driver (
       dni              VARCHAR (15) PRIMARY KEY NOT NULL,       
       name             VARCHAR (100) NOT NULL, -- `name' debería derivarse del DNI si se logra cruzar la información con otra fuente de info.
       driver_license   VARCHAR (45) NOT NULL,
       home_phone       VARCHAR (15),
       mobile_phone     VARCHAR (15),
       address          VARCHAR (355),             
       path_to_photo    VARCHAR,  -- OJO! que si cambias el directorio base de las imagenes en -- idtaxi/main.py hay que q hacerlo previamente en la base de datos tambien.
       is_active        BOOLEAN NOT NULL DEFAULT TRUE,
       created_by     VARCHAR (100),
       created_on     TIMESTAMP,
       modified_by    VARCHAR (100),
       modified_on    TIMESTAMP
);

CREATE TABLE package_store (
       id            SERIAL PRIMARY KEY NOT NULL,
       user_id       VARCHAR (100) NOT NULL, -- el usuario que realizo la venta de licencia
       driver_id     VARCHAR (15), -- licencia individual
       company_id    VARCHAR (15), -- licencia por empresas
       num_qrs       INTEGER DEFAULT 0, -- la cantidad de qrs vendidas
       due_date      TIMESTAMP, -- fecha de vencimiento
       is_closed     BOOLEAN NOT NULL DEFAULT FALSE, -- me indicaria si se completo la venta de qrs segun el numero de qrs asignadas
       is_active     BOOLEAN NOT NULL DEFAULT TRUE,
       created_by  VARCHAR (100), 
       created_on  TIMESTAMP,
       modified_by VARCHAR (100),
       modified_on TIMESTAMP,
       CONSTRAINT package_store_user_fkey FOREIGN KEY (user_id)
                REFERENCES sy_user (email) MATCH SIMPLE
                ON UPDATE NO ACTION ON DELETE NO ACTION,
       CONSTRAINT package_store_dni_fkey FOREIGN KEY (driver_id)
                REFERENCES driver (dni) MATCH SIMPLE
                ON UPDATE NO ACTION ON DELETE NO ACTION,
       CONSTRAINT package_store_ruc_fkey FOREIGN KEY (company_id)
                REFERENCES company (ruc) MATCH SIMPLE
                ON UPDATE NO ACTION ON DELETE NO ACTION

);


CREATE TABLE uuid_store (
       id            SERIAL PRIMARY KEY NOT NULL,
       user_id       VARCHAR (100) NOT NULL, -- el usuario que se le asigno la qr_uuid
       qr_uuid       UUID UNIQUE NOT NULL,
       package_id    INTEGER,
       is_assigned   BOOLEAN NOT NULL DEFAULT FALSE, -- flag para saber si la qr se asocio a un vehiculo
       is_active     BOOLEAN NOT NULL DEFAULT TRUE,
       created_by    VARCHAR (100),
       created_on    TIMESTAMP,
       modified_by   VARCHAR (100),
       modified_on   TIMESTAMP,       
       CONSTRAINT uuid_store_user_fkey FOREIGN KEY (user_id)
                REFERENCES sy_user (email) MATCH SIMPLE
                ON UPDATE NO ACTION ON DELETE NO ACTION,
       CONSTRAINT uuid_store_package_fkey FOREIGN KEY (package_id)
              REFERENCES package_store (id) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Si vehicle tiene nuevo driver, o driver conduce otro vehículo?
CREATE TABLE vehicle_driver (
       vehicle_id        VARCHAR (15) PRIMARY KEY NOT NULL,
       driver_id         VARCHAR (15) NOT NULL,
       company_id        VARCHAR (15),
       package_id        INTEGER NOT NULL, -- el numero de la licencia vendida
       qr_uuid           UUID UNIQUE NOT NULL,
       is_active         BOOLEAN NOT NULL DEFAULT TRUE,
       created_by      VARCHAR (100),
       created_on      TIMESTAMP,
       modified_by     VARCHAR (100),
       modified_on     TIMESTAMP,       
       CONSTRAINT vehicle_driver_vehicle_fkey FOREIGN KEY (vehicle_id)
       		  REFERENCES vehicle (plate) MATCH SIMPLE
       		  ON UPDATE NO ACTION ON DELETE NO ACTION,
       CONSTRAINT vehicle_driver_dni_fkey FOREIGN KEY (driver_id)
       		  REFERENCES driver (dni) MATCH SIMPLE
		         ON UPDATE NO ACTION ON DELETE NO ACTION,
       CONSTRAINT vehicle_driver_ruc_fkey FOREIGN KEY (company_id)
       		  REFERENCES company (ruc) MATCH SIMPLE
		         ON UPDATE NO ACTION ON DELETE NO ACTION,
       CONSTRAINT vehicle_driver_package_fkey FOREIGN KEY (package_id)
              REFERENCES package_store (id) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- SUPER WARNING
-- uuid no pueden ser reusados, una vez asignados & generados los sticker con el QR, ahí quedan.
-- Hay que generar nuevos! si no se pierde el historial de escaneos!!
CREATE TABLE scan_event (
       id    		VARCHAR NOT NULL,
       qr_uuid	      UUID NOT NULL,
       latitude 	      FLOAT,
       longitude	      FLOAT,
       address          VARCHAR,
       created_on       TIMESTAMP,
       PRIMARY KEY   (id)
);
