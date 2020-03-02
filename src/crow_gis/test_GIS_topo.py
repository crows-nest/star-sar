#! /usr/bin/python3
from crow_gis.GIS_topo import GIS_topo

import unittest


class TestGISTopo(unittest.TestCase):

    def test_generic(self):

        GIS_obj = GIS_topo(file="n40_w106_1arc_v3.tif")




if __name__ == "__main__":
    unittest.main()
