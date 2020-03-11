#! /usr/bin/python3

import unittest

from crow_models.human_motion import get_neighbor_gradients

array_topo_test = [4000, 4002, 4005]


class test_functions(unittest.TestCase):

    def test_get_neighbor_gradients(self):

        GIS_obj = GIS_topo()
        
        dir_path = dirname = os.path.dirname(os.path.realpath(__file__))

        dir_path = dir_path.split("crow_models")[0]
        filename = os.path.join(dir_path, 'crow_gis/n40_w106_1arc_v3.tif')

        src_ds = GIS_obj.open_geotiff(filename)
        array_depth = GIS_obj.extract_depth_np(src_ds)

        mini_array = array_depth[1000:1100, 1000:1100]

        


if __name__ == "__main__":

    unittest.main()