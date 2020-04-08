#! /usr/bin/python3

import os
import sys
import json

import matplotlib.pyplot as plt
import numpy as np
import affine
import math

class GIS_proxy(object):
    """
    empty skeleton to be filled later
    """
    
    def __init__(self):
        
        self.gis_dict = {}


    def load_data(self, filename):

        file_path = self._format_filepath_json(filename)
        with open(file_path) as json_file:
            self.gis_dict = json.load(json_file)
        
        self._numpify_data()
        
    def _numpify_data(self):

        for key in self.gis_dict.keys():
            self.gis_dict[key]["data"] = np.asarray(self.gis_dict[key]["data"])
            
    def _format_filepath_json(self, filename):
         
        if filename.endswith('.json'):
            pass
        else:
            filename += ".json"
         
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path += "/data/" + filename
        return file_path
   
    def plot_raster(self, list_graph):
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

    def get_layer(self, layer):
        return self.gis_dict[layer]

    def get_pixel_coord(self, geo_coord, dict_map):
        x, y = geo_coord[0], geo_coord[1]
        geotransform = self._geotransform(dict_map)
        fwd = affine.Affine.from_gdal(*geotransform)
        rev = ~fwd
        px, py = rev * (x, y)
        px, py = int(px + 0.5), int(py + 0.5)
        pixel_coord = (px, py)
        return pixel_coord

    def get_geo_coord(self, index, dict_map):
        geotransform = self._geotransform(dict_map)
        fwd = affine.Affine.from_gdal(*geotransform)
        coord = fwd * index
        return coord

    def _geotransform(self, dict_map):
        resolution = dict_map["resolution"]
        ulx = float(dict_map["data_bound_box"]["ulx"])
        uly = float(dict_map["data_bound_box"]["uly"])
        geotransform = (ulx, resolution["x"], 0, uly, 0, resolution["y"])
        return geotransform

    def get_dist_coord(self, coord1, coord2):
        return self._haversine(coord1, coord2)

    def _haversine(self, coord1, coord2):
        R = 6372800  # Earth radius in meters
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        phi1, phi2 = math.radians(lat1), math.radians(lat2) 
        dphi       = math.radians(lat2 - lat1)
        dlambda    = math.radians(lon2 - lon1)
        
        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


def open_json(configfile):

    file_path = os.path.dirname(os.path.realpath(__file__))
    filename = file_path + "/configs/" + configfile
    json_file = open(filename)
    json_data = json.load(json_file)
    return json_data


if __name__ == "__main__":

    #quick scripting to make sure shit works

    json_data = open_json("config_1.json")
    data_proxy = GIS_proxy()
    data_proxy.load_data(json_data["proxy_gis_filename"])
    graph_list = [data_proxy.gis_dict["depth"]["data"]]
    data_proxy.plot_raster(graph_list)



