#! /usr/bin/python3

import unittest

from human_motion import human_motion_model

from GIS_proxy import GIS_proxy, open_json


json_data = open_json("blender_osm_1.json")
data_proxy = GIS_proxy()
data_proxy.load_data(json_data["proxy_gis_filename"])




class test_functions(unittest.TestCase):

    def test_init(self):
        

        config = {"num_samples":1000, "time_steps":300}
        human_model = human_motion_model()
        
        depth_data = data_proxy.get_layer("depth")["data"]
        trails_data = data_proxy.get_layer("trails")["data"]


        sample_space = human_model.execute_mcmc(data_proxy, **config)
        

        data_proxy.plot_raster([sample_space, depth_data, trails_data])
        #gmm = human_model.gmm_from_samples(sample_space)

        #human_model.plot_gmm_depth(gmm, depth_data, sample_space)
        


if __name__ == "__main__":

    unittest.main()