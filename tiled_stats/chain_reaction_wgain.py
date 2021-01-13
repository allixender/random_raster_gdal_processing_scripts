#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

import logging
import datetime

log_level = logging.INFO
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

fh = logging.FileHandler('script_output_generate_yearly_tc_wgain_tifs.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

from subprocess import Popen, PIPE, call

tree_cover_start = "../tree_cover_gain_merged_c2_classified_nodata.tif"

start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("initialising with ... {} ... at {}".format(tree_cover_start, start))
logger.info("initialising with ... {} ... at {}".format(tree_cover_start, start))

for i in range(12, 18, 1):
    first_year_value = "../wo_nodata_amz_prode_NA_utm_corrected_value{}.tif".format(i)
    year_output = "../wo_nodata_tree_cover_30_wgain_20{0:02d}.tif".format(i)

    gdal_cmd = "gdal_calc.py -A {} -B {} --outfile={} --calc=\"A*(B==0)\" --NoDataValue=255 --type=Byte --co GDAL_NUM_THREADS=4 --co GDAL_CACHEMAX=10000 --co COMPRESS=LZW --overwrite".format(tree_cover_start, first_year_value, year_output)

    print(gdal_cmd)
    logger.info(gdal_cmd)
    p1 = Popen(gdal_cmd, shell=True, stdout=PIPE)
    # print(p1.communicate())
    logger.info(p1.communicate())
    # subprocess.Popen(["echo", year_output], stdout = subprocess.PIPE).communicate()[0]
    # print(call(gdal_cmd, shell=True))
    tree_cover_start = year_output
    print("finished this metric calculation .. {}".format( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    logger.info("finished this metric calculation .. {}".format( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
