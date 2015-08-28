select * from usuario;
select * from conductor;
select * from empresa;
select * from scan_event;
select * from uuid_store;
select * from vehiculo;
select * from vehiculo_conductor;
SELECT uuid_in(md5(now()::text)::cstring);

#insert into uuid_store (uuid,created_on) values (uuid_in(md5((NOW()+1*interval'1 day')::text)::cstring),now());
#insert into uuid_store (uuid,created_on) values (uuid_in(md5((NOW()+2*interval'1 day')::text)::cstring),now());
# bloque anonimo
DO LANGUAGE plpgsql $$
BEGIN
    FOR i IN 1..50 LOOP
        insert into uuid_store (uuid,created_on) values (uuid_in(md5((NOW()+i*interval'1 day')::text)::cstring),NOW());
    END LOOP;
END
$$;

delete from conductor;
delete from vehiculo;