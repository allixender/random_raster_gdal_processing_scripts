#!/bin/bash

gdal_calc.py -A amz_prode_NA_utm.tif -B tree_cover_30_classified.tif --outfile=amz_prode_NA_utm_corrected.tif --calc="0*(B<=1)+A*(B>=2)" --NoDataValue=0 --type=Byte
