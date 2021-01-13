#!/bin/bash

gdalwarp -ot Byte -srcnodata 0 -dstnodata 0 -multi -cutline indian_cons_reserves_utm_merged.shp -crop_to_cutline -of GTiff amz_prode_NA_utm_corrected.tif amz_prode_NA_utm_corrected_conservation_reserves_2.tif


