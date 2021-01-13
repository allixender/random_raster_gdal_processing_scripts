# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:21:38 2018

@author: Alexander
"""

# Import base libraries
from lcmodel import LC_Initialize, compute_simple_statistics
import pandas as pd
import numpy as np

import timeit

# initialise the calculator


# raster = "extract_utm.tif"
raster = "amz_prode_NA_utm.tif"

lc_calc = LC_Initialize(raster)

# simple statistics

# smp = compute_simple_statistics(lc_calc)
# smp.to_csv('simple_metrics.csv', sep=';')

# compute the desired land cover statistics

# 'Euclidean Nearest-Neighbor Distance' will still blow up,

desired_funcs = ['Land cover',
    'Edge length',
    'Edge density',
    'Number of Patches',
    'Median patch area',
    'Mean patch perimeter']

print("we will work with  {} classes".format(len(lc_calc.classes)))
print(lc_calc.classes)

# 'Like adjacencies'
print(desired_funcs)

# initialise empty dict
results_dict = {}
results_dict['class'] = []

for smt in desired_funcs:
    results_dict[smt] = []

for cli in lc_calc.classes:

    print("doing stuff for lc class {}".format(cli))
    # need to initialise cl_array and labelled_array for current class
    lc_calc.create_cl_array_for_class(cli)
    lc_calc.f_ccl(lc_calc.cl_array)

    results_dict['class'].append(cli)

    for smt in desired_funcs:
        print("next metric is {}".format(smt))
        met_tup = lc_calc.execSingleMetric(smt, cli)
        print(met_tup)
        results_dict[smt].append(met_tup[1])

# d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=results_dict)
df.to_csv('lc-stats.csv', sep=';')
print(df.head(5))


