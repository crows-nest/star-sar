#! /usr/bin/python3

from osgeo import gdal, ogr
import sys
import numpy as np

'''GDAL gotcha'''
gdal.UseExceptions()    # Enable exceptions


class GIS_topo(object):
    """
    abstraction of GDAL raster object
    prefered as topology only
    abstraction of vector types too? 
    """


    def __init__(self, filename=None):
        self.filename = filename
        self.origin = []
        self.scale = []
        self.unit_type = None

        if filename == None:
            print("GIS obj initialized no file opened")
            return


    
    def open_geotiff(self, filename):

        self.filename = filename
        src_ds = gdal.Open(filename)

        if src_ds is None:
            print('Unable to open INPUT.tif')
            return
        
        print(f"GIS file {filename} opened")

        return src_ds

    def extract_depth_np(self, src_ds, raster_band = 1):

        raster_band = src_ds.GetRasterBand(raster_band)
        np_array = raster_band.ReadAsArray()
        np_array = np.asarray(np_array)

        array_shape = np_array.shape

        print(f"converted raster {raster_band} into numpy arrray  of size {array_shape}")

        return np_array
    

        





        

        


