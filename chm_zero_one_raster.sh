#!/bin/bash

SRC_PATH=/media/rocket_gis/kmoch/nomograph/chm_zones

for i in $(seq 1 22); do
    gdal_calc.py -A $SRC_PATH/chm_5m_pzone_${i}.tif --A_band 1 --outfile=$SRC_PATH/chm_5m_pzone_${i}_zeroed.tif --co COMPRESS=LZW --calc="0*(A==0)+1*(A>0)" --type Byte

    # --NoDataValue=

done
