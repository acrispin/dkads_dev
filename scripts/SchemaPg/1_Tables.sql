
-- dbSinergyWMSbase

----------------------------------------- seguridad

-- usuarios
CREATE TABLE "public"."sy_user"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"username" VARCHAR(20),
	"email" VARCHAR(50),
	"name" VARCHAR(100),
	"passwd" VARCHAR(100),
	"active" BOOLEAN,
	"reg_date" TIMESTAMP,
	"reg_user" VARCHAR(50),
	"mod_date" TIMESTAMP,
	"mod_user" VARCHAR(50)
	);

-- roles
CREATE TABLE "public"."sy_role"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"name" VARCHAR(50),
	"active" BOOLEAN,
	"reg_date" TIMESTAMP,
	"reg_user" VARCHAR(20),
	"mod_date" TIMESTAMP,
	"mod_user" VARCHAR(20)
	);

-- roles por usuario
CREATE TABLE "public"."sy_user_role"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"sy_user_id" INTEGER,
	"sy_role_id" INTEGER
	);


----------------------------------------- almacen

-- tabla de articulos article
CREATE TABLE "public"."art"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"code" VARCHAR(20),
	"name" VARCHAR(100),
	"active" BOOLEAN,
	"reg_date" TIMESTAMP,
	"reg_user" VARCHAR(20),
	"mod_date" TIMESTAMP,
	"mod_user" VARCHAR(20)
	);

-- tabla de almacenes, warehouse
CREATE TABLE "public"."whs"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"name" VARCHAR(100),
	"active" BOOLEAN,
	"reg_date" TIMESTAMP,
	"reg_user" VARCHAR(20),
	"mod_date" TIMESTAMP,
	"mod_user" VARCHAR(20)
	);


-- tabla de motivos de movimientos o tipo de transaccion, reason
CREATE TABLE "public"."rsn"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"name" VARCHAR(100),
	"sgn" SMALLINT, -- 1: ingreso, -1: salida
	"active" BOOLEAN,
	"reg_date" TIMESTAMP,
	"reg_user" VARCHAR(20),
	"mod_date" TIMESTAMP,
	"mod_user" VARCHAR(20)
	);

-- tabla para guardar informacion de stock por almacen y material
CREATE TABLE "public"."whs_art"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"whs_id" INTEGER,
	"art_id" INTEGER,
	"qty" NUMERIC(18, 2),
	"reg_date" TIMESTAMP,
	"reg_user" VARCHAR(20),
	"mod_date" TIMESTAMP,
	"mod_user" VARCHAR(20)
	);

-- para registrar todos los movimientos de almacen
CREATE TABLE "public"."whs_tran"( 
	"_id" SERIAL PRIMARY KEY NOT NULL,
	"whs_id" INTEGER,
	"art_id" INTEGER,
	"rsn_id" INTEGER,
	"rem_gui" VARCHAR(20), -- guia de remision
	"qty" NUMERIC(18, 2),
	"active" BOOLEAN,
	"reg_date" TIMESTAMP,
	"reg_user" VARCHAR(20),
	"mod_date" TIMESTAMP,
	"mod_user" VARCHAR(20)
	);