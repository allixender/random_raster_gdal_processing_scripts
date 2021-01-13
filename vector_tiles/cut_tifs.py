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

fh = logging.FileHandler('script_output.log')
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


def cut_line(featureid, maintiff) -> str:
    # logger.info("cut tile from main with gdal cutline")
    # logger.info("run lcmodel stats over the tile and store result table")

    gdal_cmd = "gdalwarp -cutline {}.shp -crop_to_cutline {} tree_cover_c2_tile_{}.tif".format(
        featureid, maintiff, featureid)
    # logger.info(gdal_cmd)
    # subprocess.Popen(["echo", year_output], stdout = subprocess.PIPE).communicate()[0]
    # call(gdal_cmd, shell=True)
    p1 = Popen(gdal_cmd, shell=True, stdout=PIPE)
    logger.info(p1.communicate())

    return featureid


if __name__ == '__main__':
    mp.freeze_support()

    num_cores: int = mp.cpu_count()
    pool = mp.Pool(processes=num_cores-8)
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "initialising at ... {} with num cores: {}".format(start, num_cores))

    fishnet = "calc_grid_10km_basic.shp"
    rasterfile = "../tree_cover_30_classified_c2.tif"

    # Run processes
    results: Sequence[str] = [pool.apply(
        cut_line, args=(x, rasterfile,)) for x in yield_features(fishnet)]

    pool.close()

    # Get process results
    end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("finished at ... {}, with results: {}".format(
        end, len(results)))
