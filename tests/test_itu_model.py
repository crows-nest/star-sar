#! /usr/bin/python3
from crow_rf.itu_model import ITUModel

import unittest

F_GSM =  .9   #GSM frequency


class TestITUModel(unittest.TestCase):

    def test_ITU_model_attenuation(self):
        ITU_obj = ITUModel()
        ITU_func = ITU_obj.ITU_model_attenuation

        
        self.assertAlmostEqual( ITU_func(1, 1, F_GSM, 2, 50, 20), 
                                -36.53, 
                                places=2)

        self.assertAlmostEqual( ITU_func(1, 2, F_GSM, 2, 20, 50), 
                                42.90, 
                                places=2)

        
if __name__ == "__main__":
    unittest.main()

