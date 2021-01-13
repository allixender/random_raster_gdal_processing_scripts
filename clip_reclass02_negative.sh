#!/bin/bash

gdal_calc.py -A amz_prode_NA_utm.tif -B tree_cover_30_classified.tif --outfile=amz_prode_NA_utm_negative_years.tif --calc="A*(B<=1)+0*(B>=2)" --NoDataValue=0 --type=Byte

gdal_calc.py -A amz_prode_NA_utm.tif -B tree_cover_30_classified.tif --outfile=amz_prode_NA_utm_negative_binary.tif --calc="1*(B<=1)+0*(B>=2)" --NoDataValue=0 --type=Byte
