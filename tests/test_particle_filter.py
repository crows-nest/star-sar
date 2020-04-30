#! /usr/bin/python3

import unittest

from particle_filter import particle_filter
from human_motion import human_motion_model

from GIS_proxy import GIS_proxy, open_json


#use the smaller dataset for initial testing
json_data = open_json("config_1.json")
data_proxy = GIS_proxy()
data_proxy.load_data(json_data["proxy_gis_filename"])


class test_functions(unittest.TestCase):

    def test_prototype(self):
        
        p_filter = particle_filter()

        config = {"init_num_samples":100, "geo_loc":(-105.2, 40.025)  }
        human_model = human_motion_model(data_proxy, **config)
        human_model.predict_path(50)
        
        sample_array = []
 
        for path_obj in human_model.array_path_objs:
            sample_array.append(path_obj.get_curr_loc())
        
        






if __name__ == "__main__":

    
    unittest.main()