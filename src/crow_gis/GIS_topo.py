#! /usr/bin/python3

import matplotlib.pyplot as plt

from osgeo import gdal, ogr
import sys
import numpy as np
import json

'''GDAL gotcha'''
gdal.UseExceptions()    # Enable exceptions


class GIS_topo(object):
    """
    abstraction of GDAL raster object
    prefered as topology only
    abstraction of vector types too? 
    """


    def __init__(self, configfile="config_1.json"):

        json_file = open(configfile)
        json_data = json.load(json_file)


        self.filename = json_data["filename_depth"]
        self.cord_of_interest = json_data["cord_of_interest"]
        
       
        self.src_ds = self.open_geotiff(self.filename)

        print(self.extract_AOE(self.src_ds, self.cord_of_interest))


    
    
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
    
    def extract_AOE(self, src_ds, cord_of_interst):
        
        np_depth = self.extract_depth_np(src_ds)

        ulx, xres, xskew, uly, yskew, yres  = src_ds.GetGeoTransform()

        index_ulx = [(cord_of_interst["ulx"] - ulx)/xres, 
                    (cord_of_interst["lrx"] - cord_of_interst["ulx"])/xres]
        index_ulx[1] += index_ulx[0]
        index_ulx[0] = int(index_ulx[0])
        index_ulx[1] = int(index_ulx[1])


        index_y = [(cord_of_interst["uly"] - uly)/yres, 
                    (cord_of_interst["lry"] - cord_of_interst["uly"])/yres]

        index_y[1] += index_y[0]
        index_y[0] = int(index_y[0])
        index_y[1] = int(index_y[1])

        #sliced_depth_y = np_depth[index_y[0]:index_y[1], :]
        #sliced_depth_x = np_depth[:, index_ulx[0]:index_ulx[1]]
        
        aoe = np_depth[index_y[0]:index_y[1], index_ulx[0]:index_ulx[1]]

        #self.plot_depth(np_depth, sliced_depth_x, sliced_depth_y, aoe)

        return aoe        


    def plot_depth(self, orig, aoe_x, aoe_y, aoe):

        fig = plt.figure()

        ax1 = fig.add_subplot(1, 4, 1)
        ax1.imshow(orig)

        ax2 = fig.add_subplot(1, 4, 2)
        ax2.imshow(aoe_x)

        ax3 = fig.add_subplot(1, 4, 3)
        ax3.imshow(aoe_y)

        ax4 = fig.add_subplot(1, 4, 4)
        ax4.imshow(aoe)


        plt.show()





        





        

        


