#! /usr/bin/python3

from osgeo import gdal, ogr
import matplotlib.pyplot as plt
import numpy as np

import affine
import sys
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

        np_aoe = self.get_AOE(self.src_ds, self.cord_of_interest)
    
    
    def open_geotiff(self, filename):

        self.filename = filename
        src_ds = gdal.Open(filename)

        if src_ds is None:
            print('Unable to open INPUT.tif')
            return
        
        print(f"GIS file {filename} opened")

        return src_ds

    def get_depth_np(self, src_ds, raster_band = 1):

        raster_band = src_ds.GetRasterBand(raster_band)
        np_array = raster_band.ReadAsArray()
        np_array = np.asarray(np_array)

        array_shape = np_array.shape

        print(f"converted raster {raster_band} into numpy arrray  of size {array_shape}")

        return np_array
    

    def get_AOE(self, src_ds, cord_of_interst):
        
        np_depth = self.get_depth_np(src_ds)

        ulx = cord_of_interst["ulx"]
        uly = cord_of_interst["uly"]
        lrx = cord_of_interst["lrx"]
        lry = cord_of_interst["lry"]


        index_ul = self.get_pixel_coord((ulx, uly), src_ds)
        index_lr = self.get_pixel_coord((lrx, lry), src_ds)
        
        #TODO out of index check numpy loops indexes

        np_aoe = np_depth[index_ul[0]:index_lr[0]:, 
                          index_ul[0]:index_lr[0]:]

        return np_aoe        

    def get_pixel_coord(self, geo_coord, src_ds):

        x, y = geo_coord[0], geo_coord[1]
        forward_transform =  \
            affine.Affine.from_gdal(*src_ds.GetGeoTransform())
        reverse_transform = ~forward_transform
        px, py = reverse_transform * (x, y)
        px, py = int(px + 0.5), int(py + 0.5)
        pixel_coord = px, py

        return pixel_coord

    def plot_depth(self, list_graph):

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





        





        

        


