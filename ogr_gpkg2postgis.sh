#!/bin/bash

ogr2ogr -progress --config PG_USE_COPY YES -f PostgreSQL PG:" dbname=$DBNAME host=$DBHOST port=5432 user=$DBUSER active_schema=geoworkspace password=$DBPASS" -lco DIM=2 /media/rocket_gis/estsoil-eh_soilmap/EstSoil-EH_v1.2a.gpkg EstSoil-EH_v1.2a -lco LAUNDER=NO -overwrite -lco GEOMETRY_NAME=geom -lco FID=fid -nln geoworkspace.estsoil_eh_v12a_tmp -nlt PROMOTE_TO_MULTI -select fid,orig_fid,Varv,soilcode
