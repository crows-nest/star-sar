

import numpy as np

from math import sqrt, log
from tqdm import tqdm
from sklearn import mixture

from tqdm import tqdm
from human_motion import HikerPathsObj


class ObsPathObj(object):
    """

    """

    def __init__(self, length=100, start_time=0):
        """
        length equals time, everything is 1 minute
        """

        self.data = np.zeros((length, 3), dtype=np.int16)

        self.curr_index = -1
        self.start_time = start_time

    def load_loc_array(self, loc_array: list, start_time: int):
        
        if len(loc_array) + start_time > len((self.data)):
            print("ERROR data does not fit in total time")
            return

        self.start_time = start_time

        for index, loc in enumerate(loc_array):
            time = index + start_time
            self.data[time] = (loc[0], loc[1], time)
        print(f"obs path of size:{len(loc_array)} starting:{start_time} load")

    def get_start_time(self):
        return self.start_time
    
    def get_length(self):
        return len(self.data)

    def get_k_loc(self, k):
        loc = self.data[k, 0:2]

        return tuple(loc)


class PathParticleFilter(object):   

              
    def get_trail_obs_prob(self, hiker_path_obj: HikerPathsObj, 
                           obs_path_obj: ObsPathObj)->list:
        
        log_weights = []

        obs_start = obs_path_obj.get_start_time()
        end_time = obs_path_obj.get_length()

        for sample in tqdm(hiker_path_obj.data):
            weight = 1
            for time in range(obs_start, end_time):
                obs_loc = obs_path_obj.data[time]
                target_loc = sample[time]
                prob = self.obs_uniform_round_neg(obs_loc, target_loc)
                weight *= prob
            log_weights.append(log(weight))

        return log_weights


    def weighting_func(self, weights: list):

        min_weight = min(weights) - .2
        weights = [value - min_weight for value in weights]
        return weights


    def obs_uniform_round_neg(self, o_loc, x_loc, radius=10, prob=0.99):
        """ observation of previous paths
        NOTE this returns opposite probabilities than whay you think
        the idea is that x_loc are predicted locations so if the 
        x_loc is within range no hiker is actually there this its a negative 
        observation and should devalue the weight of that path
        """
        dist = sqrt((o_loc[0]-x_loc[0])**2 + (o_loc[1]-x_loc[1])**2 )

        #observation within window
        if dist <= radius:
            
            return 1 - prob
        return prob