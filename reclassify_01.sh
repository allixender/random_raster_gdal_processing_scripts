#!/bin/bash

gdal_calc.py -A amz_tree_cover_utm.tif --outfile=tree_cover_30_classified.tif --calc="0*(A<0)+1*((A<=30)*(A>=0))+2*(A>30)" --NoDataValue=0 --type=Byte
