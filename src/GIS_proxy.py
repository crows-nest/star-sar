#! /usr/bin/python3

import os
import sys
import json

import matplotlib.pyplot as plt
import numpy as np

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
    data_proxy.plot_depth(graph_list)



