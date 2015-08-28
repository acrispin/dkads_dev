#!/bin/bash

for IMG in $(ls *.png);
do
    CODE=$(basename $IMG .png)
    psql -c "INSERT INTO uuid_store (uuid, created_on) values ('$CODE', now())" --dbname=basedb -U development
done
