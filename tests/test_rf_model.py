#! /usr/bin/python3
from rf_model import ITUModel, FriisTrans, RFModel
from GIS_proxy import open_json, GIS_proxy
import unittest

FULL_TEST = 0

F_GSM =  .9   #GSM frequency

json_data = open_json("blender_osm_1.json")
data_proxy = GIS_proxy()
data_proxy.load_data(json_data["proxy_gis_filename"])

class TestFullRFModel(unittest.TestCase):

    @unittest.skipUnless(FULL_TEST, 1)
    def test_ITU_model_attenuation(self):
        ITU_obj = ITUModel()
        ITU_func = ITU_obj.ITU_model_attenuation

        self.assertAlmostEqual(ITU_func(1, 1, F_GSM, 2, 50, 20), 
                               -36.53, places=2)

        self.assertAlmostEqual(ITU_func(1, 2, F_GSM, 2, 20, 50), 
                               42.90, places=2)
    
    @unittest.skipUnless(FULL_TEST, 1)
    def test_friis_conversion(self):
        transmission_obj = FriisTrans()
        mhz_to_lambda = transmission_obj.mhz_to_lambda
        self.assertAlmostEqual(mhz_to_lambda(2400), 0.12491352, places=4)
                               
    @unittest.skipUnless(FULL_TEST, 1)
    def test_friis_model(self):
        fris_model = FriisTrans()
        func_power = fris_model.power_received
        self.assertAlmostEqual(func_power(100), -60.05, places=2)
        self.assertAlmostEqual(func_power(400), -72.09, places=2 )
        self.assertAlmostEqual(func_power(1000), -80.05, places=2 )
        self.assertAlmostEqual(func_power(2000), -86.07, places=2 )

    @unittest.skipUnless(FULL_TEST, 1)
    def test_haversine(self):
        func_dist = data_proxy._haversine
        geo1 = (-105.299, 40.0143)
        geo2 = (-105.27, 40.016)
        self.assertAlmostEqual(func_dist(geo1, geo2), 3225.9, places=0)

    @unittest.skipUnless(FULL_TEST, 1)
    def test_geocoord(self):
        dict_depth = data_proxy.get_layer("depth")
        test_geo = (-105.33, 40.05)
        index = data_proxy.get_pixel_coord(test_geo, dict_depth)
        geo_back = data_proxy.get_geo_coord(index, dict_depth)

        self.assertAlmostEqual(test_geo[0], geo_back[0], places=2)
        self.assertAlmostEqual(test_geo[1], geo_back[1], places=2)

    @unittest.skipUnless(FULL_TEST, 1)
    def test_get_dist_coor(self):
        func_dist = data_proxy.get_dist_coord

        coord_1, coord_2  = (-105.38, 40.05), (-105.38, 40.0)
        self.assertAlmostEqual(func_dist(coord_1, coord_2), 5.55, places=0)
        self.assertAlmostEqual(func_dist(coord_2, coord_1), 5.55, places=0)
        coord_1, coord_2  = (-105.38, 40.00), (-105.33, 40.0)
        self.assertAlmostEqual(func_dist(coord_1, coord_2), 4.25, places=0)
        self.assertAlmostEqual(func_dist(coord_2, coord_1), 4.25, places=0)

  
    def test_RFModel(self):
        
        print(data_proxy.gis_dict["depth"]["data_bound_box"])
        geo_loc = (-105.308, 40.0549)
        rf_model = RFModel(data_proxy)  
        prob_map = rf_model.binary_threshold_map(geo_loc, -70)

        depth_map = data_proxy.get_layer("depth")["data"]

        data_proxy.plot_raster([prob_map, depth_map])




if __name__ == "__main__":
    unittest.main()

