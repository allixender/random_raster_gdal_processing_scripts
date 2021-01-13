#!/bin/bash

gdalwarp -ot Byte -srcnodata 0 -dstnodata 0 -wm 12000 -multi -cutline processing_cons.shp -crop_to_cutline -of GTiff amz_prode_NA_utm_corrected.tif amz_prode_NA_utm_corrected_conservation_reserves.tif

gdalwarp -ot Byte -srcnodata 0 -dstnodata 0 -wm 12000 -multi -cutline processing_india.shp -crop_to_cutline -of GTiff amz_prode_NA_utm_corrected.tif amz_prode_NA_utm_corrected_indian_reserves.tif

