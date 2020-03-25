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
        Initializes GIS object, loads JSON file contains "filename_depth", 
        "data_bounding_box"
        
        Parameters
        ----------
        configfile : str, optional
            the JSON file to load configurations from, by default 
            "config_1.json"
        """

        json_data = self.open_json(configfile)

        self.filename_depth = json_data["filename_depth"]
        self.data_bounding_box = json_data["data_bounding_box"]
        
        # GIS dictionary object will contain all the neccessary GIS data for
        # use with the GIS_proxy.
        self.gis_dict= {}

    def write_gis_dict_json(self, filename):
        """
        write gis_dict json
        
        Parameters
        ----------
        filename : str
            filename to write json as
        """

        file_path = self._format_filepath_json(filename)
        json_dict = self.gis_dict

        #JSON cannot format numpy array
        for layer in json_dict:
            json_dict[layer]["data"] = json_dict[layer]["data"].tolist()
        
        with open(file_path, "w") as outfile:
            json.dump(json_dict, outfile)

    def read_gis_dict_json(self, filename):
        """
        load a gis_dict json file
        
        Parameters
        ----------
        filename : str
            
        """
        
        file_path = self._format_filepath_json(filename)
        with open(file_path) as json_file:
            self.gis_dict = json.load(json_file)
        
    def _format_filepath_json(self, filename):
        """
        format filename to include absolute pathing relative to the GIS_import
        script
        
        Parameters
        ----------
        filename : str
            filename to json format
        
        Returns
        -------
        str
            absolute pathing for filename
        """
         
        if filename.endswith('.json'):
            pass
        else:
            filename += ".json"
         
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path += "/data/" + filename
        return file_path
    
    def add_dict(self, dict_data, key):
        """
        adds dictionary to gis_dict with the key value given
        acceptable key values are "depth" and "trail"
        
        Parameters
        ----------
        dict_data : dict
            
        key : str
            key value to pull up data dictionary
        """
        #simple check for overwritting data
        if key in self.gis_dict.keys():
            tmp = input("dictionary already present overwrite? Y/n")
            for char in tmp:
                if char == "y" or "Y":
                    print(f"overwrite: {key}")
                    self.gis_dict[key] = dict_data
                    break
                elif char == "n" or "N":
                    print(f"do not overwrite: {key}")
                    break            
                print(f"invalid character: {char}")
        else:
            print(f"write {key} to gis_dict")
            self.gis_dict[key] = dict_data

    def build_geotiff_to_dict(self, filename, data_bounding_box):
        """
        uses geotiff to build dataset dictionary
        
        Parameters
        ----------
        filename : str
            filename to loaf geotiff data from
        data_bounding_box : dict
            
        
        Returns
        -------
        dict
            dictionray with depth data and parameters
        """

        depth_dict = {}
        geotiff_ds = self.open_geotiff(filename)
        geotransform = geotiff_ds.GetGeoTransform()
        X_res = geotransform[1]
        y_res = geotransform[5]
        np_aoi = self.get_AOI(geotiff_ds, data_bounding_box)

        depth_dict["data"] = np_aoi
        depth_dict["data_bound_box"] = data_bounding_box
        depth_dict["resolution"] = {"x": X_res ,"y": y_res }
        return depth_dict

    def open_json(self, configfile):
        """
        open JSON file and return dictionary of values
        
        Parameters
        ----------
        configfile : str
            name of config file to use
        
        Returns
        -------
        dict
            dictionary of JSON data
        """
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

        filename = file_path + "/data/" + filename
        print(filename)
        src_ds = gdal.Open(filename)

        if src_ds is None:
            print('Unable to open INPUT.tif')
            return
        
        print(f"GIS file {filename} opened")

        return src_ds

    def get_depth_np(self, src_ds, raster_band = 1):
        """
        uses a GDAL raster dataset to open first raster band and turn into 
        numpy array
        
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

        print(f"converted raster {raster_band} into numpy arrray  of size 
        {array_shape}")

        return np_array
    
    def get_AOI(self, src_ds, cord_of_interst):
        """
        using th GDAL dataset returns the area define by data_bounding_box 
        dict. the cord are defined in terms of lat and long
        no errors for out if bounds cordinates
        #TODO out of bounds errors? probably not worth the effort now
        Parameters
        ----------
        src_ds : GDAL raster dataset
            GDAL raster object
        cord_of_interst : dict
            dictionary of coordinates contains: ulx, uly, lrx, lry 
            (Upper Left and Lower Right)
        
        Returns
        -------
        2D numpy
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

        np_aoi = np_depth[index_ul[0]:index_lr[0]:, 
                          index_ul[0]:index_lr[0]:]

        return np_aoi

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

    #some sample scripting to write depth 
    data_obj = GIS_import()
    depth_dict = data_obj.build_geotiff_to_dict(data_obj.filename_depth, 
                                                data_obj.data_bounding_box)

    data_obj.add_dict(depth_dict, "depth")
    data_obj.write_gis_dict_json("depth_boulder.json")

    