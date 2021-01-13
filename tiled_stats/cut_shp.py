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
import sys, os

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

outfolder = os.path.join("..", "vector_tiles")

with fiona.open(path="calc_grid_10km_basic.shp") as shp:
    myschema = shp.schema
    logger.info(myschema)
    
    mycrs = shp.crs
    logger.info(mycrs)
    for feat in shp:
        id = feat.get("id")
        # logger.info(str(id))
        with fiona.open(os.path.join(outfolder,str(id) + '.shp'), 'w',crs=mycrs,driver='ESRI Shapefile', schema=myschema) as output:
            output.write(feat)


end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info("finished at ... {}".format(end))
