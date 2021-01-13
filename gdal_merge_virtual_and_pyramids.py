import os
import subprocess
import sys
from pathlib import Path

# you need gdal installed, but for this script to use some extra features,
# you might want to have gdal python bindings installed, but not needed for the merge
from osgeo import gdal

# this allows GDAL to throw Python Exceptions, not needed for the merge
gdal.UseExceptions()

filelist = []

for filename in os.listdir('.'):
    # go into the folders starting with ... to find the TIFFs
    if filename.startswith("ESM2012_Rel2017"):

        # it's very specific use case here, these nested folders
        tifval = filename.replace('ESM2012_Rel2017_', '')
        longpath = os.path.join(filename, tifval)
        thistif = os.path.join(longpath, tifval + '.TIF')
        try:
            Path(thistif).resolve()
        except FileNotFoundError:
            sys.exit(thistif + ' doesnt exist?')

        else:
            # if you want to check if the file can be opened by gdal, not needed for the merge
            # raster = gdal.Open(thistif)
            filelist.append(thistif)
    else:
        print("skipping file: " + filename)

for filename in filelist:
    print("using file: " + filename)
    subprocess.run(["/usr/bin/gdalinfo", filename])

# instead of copying uncompressing memory-crashing working with big geotiffs directly,
# you can build a virtual geotiff by linking them together
# the VRT file is only an XML description of the linkage and some parameters
vrt_cmd = ["/usr/bin/gdalbuildvrt", "-vrtnodata", "256", "-r", "nearest", "vrt_merged_raster.vrt"]
vrt_build = vrt_cmd + filelist

print("starting cmd 1: {}".format(" ".join(vrt_build)))
# subprocess.run(vrt_build)

# this virtual linkage file can then serve as input for gdal tools, like gdalwarp, gdal_translate etc
# here we just
# -expand gray ; -r nearest; -colorinterp gray .. >= 2.3-stats; "-co", "USE_TIF_OVR=TRUE"?
gdaltranslate_cmd = ["/usr/bin/gdal_translate", "-ot", "UInt16",  "-of", "Gtiff",
                     "-r", "nearest", 
                     "-mo", "DataRepresentation=THEMATIC", "-mo", "DataType=Thematic",
                     "-mo", "BandName=Band_1", 
                     "-co", "BIGTIFF=YES", "-co", "COMPRESS=LZW",
                     "-co", "GDAL_CACHEMAX=16240", "-co", "GDAL_NUM_TRHEADS=4", "-co", "TFW=YES",
                     "-stats", "vrt_merged_raster.vrt", "spain_merged.tif"]
print("starting cmd 2: {}".format(" ".join(gdaltranslate_cmd)))
# subprocess.run(gdaltranslate_cmd)

# inspired by https://www.northrivergeographic.com/archives/pyramid-layers-qgis-arcgis
#  "-minsize", "128", is for gdal >= 2.3 not here
gdaladdo_cmd = ["/usr/bin/gdaladdo", "-r", "nearest", "-ro", "--config", "COMPRESS_OVERVIEW", "LZW", "--config",
                "BIGTIFF_OVERVIEW", "IF_SAFER", "--config", "USE_RRD", "NO", "--config", "GDAL_NUM_TRHEADS", "4",
                "--config", "TILED", "YES", "--config", "GDAL_CACHEMAX", "16240", 
                "spain_merged.tif", "2", "4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048" ,"4096"]
print("starting cmd 3: {}".format(" ".join(gdaladdo_cmd)))
# subprocess.run(gdaladdo_cmd)

gdalstats_cmd = ["/usr/bin/gdalinfo", "-stats", "-hist", "spain_merged.tif"]
print("starting cmd 4: {}".format(" ".join(gdalstats_cmd)))
# subprocess.run(gdalstats_cmd)

print("done")
