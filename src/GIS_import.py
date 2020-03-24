#! /usr/bin/python3

from osgeo import gdal, ogr
import matplotlib.pyplot as plt
import numpy as np

import os
import affine
import sys
import json

'''GDAL gotcha'''
gdal.UseExceptions()    # Enable exceptions


class GIS_import(object):
    """
    importer for GIS data using GDAL
    """

    def __init__(self, configfile="config_1.json"):
        """
        Initializes GIS object, loads JSON file contains "filename_depth", "cord_of_interest"
        
        Parameters
        ----------
        configfile : str, optional
            the JSON file to load configurations from, by default "config_1.json"
        """
    
        json_data = self.open_json(configfile)

        self.filename = json_data["filename_depth"]
        self.cord_of_interest = json_data["cord_of_interest"]
        self.src_ds = self.open_geotiff(self.filename)
      
    def open_json(self, configfile):
        file_path = os.path.dirname(os.path.realpath(__file__))

        filename = file_path + "/configs/" + configfile

        json_file = open(filename)

        json_data = json.load(json_file)

        return json_data
        
    def open_geotiff(self, filename):
        """
        loads a geotif file, file pathing is relative to exection
        TODO make global file referencing
        
        Parameters
        ----------
        filename : string
            name of geotiff file to open
        
        Returns
        -------
        GDAL raster dataset
            GDAL raster object
        """
        file_path = os.path.dirname(os.path.realpath(__file__))

        filename = file_path + "/" + filename
        print(filename)
        src_ds = gdal.Open(filename)

        if src_ds is None:
            print('Unable to open INPUT.tif')
            return
        
        print(f"GIS file {filename} opened")

        return src_ds

    def get_depth_np(self, src_ds, raster_band = 1):
        """
        uses a GDAL raster dataset to open first raster band and turn into numpy array
        
        Parameters
        ----------
        src_ds : GDAL raster dataset
            GDAL raster object
        raster_band : int, optional
            th eband to look up, by default 1
        
        Returns
        -------
        np.array
            numpy array containing the depth data
        """

        raster_band = src_ds.GetRasterBand(raster_band)
        np_array = raster_band.ReadAsArray()
        np_array = np.asarray(np_array)

        array_shape = np_array.shape

        print(f"converted raster {raster_band} into numpy arrray  of size {array_shape}")

        return np_array
    
    def get_AOE(self, src_ds, cord_of_interst):
        """
        using th GDAL dataset returns the area define by cord_of_interest dict.
        the cord are defined in terms of lat and long
        no errors for out if bounds cordinates
        
        Parameters
        ----------
        src_ds : GDAL raster dataset
            GDAL raster object
        cord_of_interst : dict
            dictionary of coordinates contains: ulx, uly, lrx, lry (Upper Left and Lower Right)
        
        Returns
        -------
        [type]
            [description]
        """
        
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
        """
        uses GDAL dataset to pull array index for a cordinate

        
        Parameters
        ----------
        geo_coord : tuple
            lat and long coordinate
        src_ds : GDAL raster dataset
            GDAL raster object
        
        Returns
        -------
        tuple
            index of geo cordinates
        """
        x, y = geo_coord[0], geo_coord[1]
        forward_transform = affine.Affine.from_gdal(*src_ds.GetGeoTransform())
        reverse_transform = ~forward_transform
        px, py = reverse_transform * (x, y)
        px, py = int(px + 0.5), int(py + 0.5)
        pixel_coord = (px, py)

        return pixel_coord

    def plot_depth(self, list_graph):
        """
        plots 2D arrays as graphs in matlplotlib
        accepts lists of 2D arrays to be graphed
        makes a subplot for each graph
        
        Parameters
        ----------
        list_graph : list
            list of 2D graphs to be displayes
        """
        
        fig = plt.figure()
        ax = []
        num_graphs = len(list_graph)

        for index, graph in enumerate(list_graph):

            ax = fig.add_subplot(1, num_graphs, index + 1)
            ax.imshow(graph)
        plt.show()


if __name__ == "__main__":

    print("hey make a script for using the importer class")

    