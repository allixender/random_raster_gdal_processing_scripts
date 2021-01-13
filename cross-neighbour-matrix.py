#!/usr/bin/python3

# Import base libraries
import os,sys,csv,string,math,operator,subprocess,tempfile,inspect

# Import numpy and scipy
import numpy as np

import gdal, ogr

rasterpath = "amz_prode_NA_utm_corrected.tif"

raster = gdal.Open(str(rasterpath))

gt = raster.GetGeoTransform()

print(gt)
pixelSizeX = gt[1]
pixelSizeY =-gt[5]
print(pixelSizeX)
print(pixelSizeY)

band = raster.GetRasterBand(1)

nodata = band.GetNoDataValue()

example_array =  band.ReadAsArray()

classes = sorted(np.unique(example_array)) # get classes

classes.remove(nodata)

print("classes: {}".format(classes))
print("array shape: {}".format(example_array.shape))
print("nodata value: {}".format(nodata))
print("dtype: {}".format(example_array.dtype))

if not "int" in str(example_array.dtype):
    raise Exception("Error only full integer classes")

matti = np.zeros((len(classes)+1,len(classes)+1), dtype=np.int64)

for i in range(len(classes)):
    matti[i+1,0] = classes[i]
    matti[0,i+1] = classes[i]

print(matti)

heightFP,widthFP = example_array.shape #define hight and width of input matrix
withBorders = np.ones((heightFP+(2*1),widthFP+(2*1)), dtype=np.int8)*nodata # set the border to borderValue
withBorders[1:heightFP+1,1:widthFP+1]=example_array # set the interior region to the input matrix

for j in range(1, example_array.shape[0]):
    for i in range(1, example_array.shape[1]):

        if not withBorders[j,i] == nodata:
            # print("withBorders[{},{}] = {}".format(j,i, withBorders[j,i]))
            # get central val class
            # that means x is the class for which we update neighbours stats in matti
            # so x is the "ref_class" and neighbours a-h are "count_classes"
            # at position matti[x,a] += 1
            x = int( withBorders[j,i] )
            # sample 8 neighbours
            # a b c
            # h x d
            # g f e
            a = int( withBorders[j-1,i-1] )
            if not a == nodata:
                matti[x,a] += 1
            b = int( withBorders[j-1,i] )
            if not b == nodata:
                matti[x,b] += 1
            c = int( withBorders[j-1,i+1] )
            if not c == nodata:
                matti[x,c] += 1
            d = int( withBorders[j,i+1] )
            if not d == nodata:
                matti[x,d] += 1
            e = int( withBorders[j+1,i+1] )
            if not e == nodata:
                matti[x,e] += 1
            f = int( withBorders[j+1,i] )
            if not f == nodata:
                matti[x,f] += 1
            g = int( withBorders[j+1,i-1] )
            if not g == nodata:
                matti[x,g] += 1
            h = int( withBorders[j,i-1] )
            if not h == nodata:
                matti[x,h] += 1
            # update matti ++ at all designations

print(matti)

np.savetxt("cross-matrix.csv", matti, delimiter=",")

