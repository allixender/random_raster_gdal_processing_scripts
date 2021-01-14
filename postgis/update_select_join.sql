select distinct "Varv" from geoworkspace.estsoil_eh_v12a_tmp order by "Varv" asc;

select estsoil_eh_v12a_tmp."Varv", estsoil_eh_v12a_tmp.orig_fid from geoworkspace.estsoil_eh_v12a_tmp, geoworkspace.estsoil_eh_v12c where estsoil_eh_v12c.orig_fid = estsoil_eh_v12a_tmp.orig_fid;

SELECT estsoil_eh_v12a_tmp."Varv" FROM geoworkspace.estsoil_eh_v12a_tmp INNER JOIN geoworkspace.estsoil_eh_v12c ON (estsoil_eh_v12a_tmp.orig_fid = estsoil_eh_v12c.orig_fid);

alter table geoworkspace.estsoil_eh_v12c add column varv int8;

    
UPDATE geoworkspace.estsoil_eh_v12c
SET varv=T12c.varv12c   
FROM (SELECT estsoil_eh_v12a_tmp."Varv" AS varv12c, estsoil_eh_v12a_tmp.orig_fid as orig12c
          FROM geoworkspace.estsoil_eh_v12a_tmp) AS T12c
    WHERE estsoil_eh_v12c.orig_fid=T12c.orig12c;
