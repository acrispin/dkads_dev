sudo -u postgres -- sh -c 'cd; dropdb basedb; createdb basedb'
psql -f schema.sql basedb development
psql -f nueva_unidad.sql basedb development
bash cook_some_qr.sh
