-- alters tables
/*

console
:~$ sudo su postgres
:~$ cd
:~$ psql
postgres=# \connect basedb
basedb=# ALTER TABLE uuid_store ADD COLUMN modified_on TIMESTAMP;

*/


ALTER TABLE uuid_store ADD COLUMN modified_on TIMESTAMP;



-- 2014-05-30
ALTER TABLE uuid_store ADD COLUMN package_id INTEGER;
ALTER TABLE uuid_store ADD CONSTRAINT uuid_store_package_fkey FOREIGN KEY (package_id) REFERENCES package_store (id);