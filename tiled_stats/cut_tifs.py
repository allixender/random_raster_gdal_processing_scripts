#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Tuple, List, Tuple, Union
from typing import NewType, Callable, Iterable
from typing import Mapping, Sequence, TypeVar, Generic, Any

import multiprocessing as mp
from subprocess import Popen, PIPE, call
import fiona  # type: ignore

import logging
import datetime
import sys

log_level = logging.INFO
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

fh = logging.FileHandler('script_output-cut_treecover2002plus.log')
console = logging.StreamHandler(sys.stdout)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
# logger.addHandler(console)
logger.addHandler(fh)

start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info("initialising at ... {}".format(start))

def yield_features(filename) -> Iterable[str]:
    with fiona.open(path=filename) as fh:
        for feat in fh:
            # print(feat)
            yield str(feat.get("id"))


def cut_line(featureid: str, maintiff: str, year: int) -> str:
    # logger.info("cut tile from main with gdal cutline")

    gdal_cmd = "gdalwarp -cutline ../vector_tiles/{}.shp -crop_to_cutline {} ../tree_cover_30_{}/tree_cover_c2_tile_{}.tif".format(
        featureid, maintiff, year, featureid)
    # logger.info(gdal_cmd)
    # subprocess.Popen(["echo", year_output], stdout = subprocess.PIPE).communicate()[0]
    # call(gdal_cmd, shell=True)
    p1 = Popen(gdal_cmd, shell=True, stdout=PIPE)
    logger.info(p1.communicate())

    return featureid


if __name__ == '__main__':
    mp.freeze_support()

    num_cores: int = int(mp.cpu_count()/2)
    fishnet="calc_grid_10km_basic.shp"

    for year in range(2002, 2018, 1):
        pool=mp.Pool(processes = num_cores)
        start=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rasterfile="../tree_cover_30_{}.tif".format(year)
        logger.info(
            "initialising at ... {} with {} cores for tif/folder: {}".format(start, num_cores, rasterfile))
        
        # Run processes
        results: Sequence[str]=[pool.apply(
            cut_line, args= (x, rasterfile, year,)) for x in yield_features(fishnet)]

        pool.close()

        # Get process results
        end=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info("finished at ... {}, with results: {}".format(
            end, len(results)))
