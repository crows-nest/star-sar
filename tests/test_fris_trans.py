#! /usr/bin/python3

from crow_rf.fris_trans import FrisTrans

import unittest

class TestFrisTrans(unittest.TestCase):

    def test_conversion(self):
        transmission_obj = FrisTrans()

        mhz_to_lambda = transmission_obj.mhz_to_lambda

        self.assertAlmostEqual(mhz_to_lambda(2400), 0.12491352, places=4)


    def test_power(self):

        transmission_obj = FrisTrans()

        power_func = transmission_obj.power_received


        
        self.assertAlmostEqual(power_func(100), -20.047, places=1)
        
        self.assertAlmostEqual(power_func(200), -26.068, places=1)

        self.assertAlmostEqual(power_func(400), -32.09, places=1)

if __name__ == "__main__":
    unittest.main()