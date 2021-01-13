#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Tuple, List, Tuple, Union
from typing import NewType, Callable, Iterable
from typing import Mapping, Sequence, TypeVar, Generic, Any

import multiprocessing as mp
from subprocess import Popen, PIPE, call
import fiona  # type: ignore

from lcmodel_typed import LC_Initialize, compute_simple_statistics
import pandas as pd  # type: ignore
import numpy as np  # type: ignore

import logging
import datetime
from operator import itemgetter
import sys
import os

log_level = logging.INFO
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

fh = logging.FileHandler('script_output-para_stats_forest_loss_no_class_single.log')
console = logging.StreamHandler(sys.stdout)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
# logger.addHandler(console)
logger.addHandler(fh)

# these are class/year based
single_metrics = ['Edge density',
                  'Mean patch area',
                  'Median patch area',
                  'Euclidean Nearest-Neighbor Distance',
                  'Like adjacencies',
                  'Overall Core area',
                  'Patch cohesion index']

# these are landscape based without class
land_metrics = ["LC_Mean",
                "LC_Min",
                "LC_Sum",
                "LC_Max",
                "LC_SD",
                "LC_LQua",
                "LC_Med",
                "LC_UQua",
                "DIV_SI"]


def yield_features(filename) -> Iterable[str]:
    with fiona.open(path=filename) as fh:
        for feat in fh:
            # print(feat)
            if str(feat.get("id")) == "32956":
                pass
            yield str(feat.get("id"))


def calculate_for_feature(featureid: str) -> Dict:
    # logger.info("run lcmodel stats over the tile and store result table")
    folder = "../forest_loss_all"
    raster = os.path.join(
        folder, "amz_prode_NA_utm_corrected_tile_{}.tif".format(featureid))

    # initialise per tile values empty dict
    results_dict: Dict[str, Union[str, float]] = {}
    results_dict['tile_id'] = featureid

    try:
        lc_calc = LC_Initialize(raster)

        lc_calc.create_cl_array_for_class(None)
        lc_calc.f_ccl(lc_calc.cl_array)

        for smt in single_metrics:
            met_tup = lc_calc.execSingleMetric(smt, None)
            results_dict[smt] = met_tup[1]

    except Exception as ex:
        logger.error(ex)
        for smt in single_metrics:
            results_dict[smt] = 0.0

    logger.info("For tile {} -> {}".format(featureid, results_dict))
    return results_dict


if __name__ == '__main__':
    mp.freeze_support()

    num_cores: int = int(mp.cpu_count()/4)
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "initialising at ... {} with num cores: {}".format(start, num_cores))

    fishnet = "calc_grid_10km_basic.shp"

    ########################################
    # initialise empty dict for land metrics
    ########################################

    # initialise empty dict
    data_dict: Dict[str, List] = {}
    data_dict['tile_id'] = []

    for smt in single_metrics:
        data_dict[smt] = []

    # Run processes for single metrics
    pool = mp.Pool(processes=num_cores)
    results: List[Dict] = [pool.apply(
        calculate_for_feature, args=(x, )) for x in yield_features(fishnet)]

    pool.close()

    sorted_results = sorted(results, key=itemgetter('tile_id'))

    for res in sorted_results:
        data_dict['tile_id'].append(res.get("tile_id"))
        for smt in single_metrics:
            data_dict[smt].append(res.get(smt))

    # d = {'tile_id': [1, 2], 'patch_area': [3, 4]} ...
    df = pd.DataFrame(data=data_dict)
    df.to_csv('lc-stats_forest_loss_noclass_single.csv', sep=';')

    # Get process results
    end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("finished at ... {}, with results: {}".format(
        end, len(sorted_results)))

