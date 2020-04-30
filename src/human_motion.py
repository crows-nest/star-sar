#! /usr/bin/python3

import os
import sys
import copy

import matplotlib.pyplot as plt
from gis_proxy import GISproxy, open_json
import numpy as np
from tqdm import tqdm
from sklearn import mixture
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import



class HikerPathsObj(object):

    def __init__(self, samples=1, length=100, start_time=0):
        #object for homgeneous length and time samples of pathing
        #all samples must have the same time location as well
        #( X, Y, time)
        #TODO currently time is meaningless and time == length index 
        self.data = np.zeros((samples, length, 3), dtype=np.int16)

        # -1 indicates un-initialized path obj
        self.curr_index = -1
        self.start_time = start_time
        
    def start_loc_all(self, start_loc: tuple):
        
        start_tuple = (start_loc[0], start_loc[1], self.start_time)
        self.data[:, 0, :] = start_tuple
        self.curr_index = 0
        print(f"initializing all to: {start_loc}")
        
    def start_loc_list(self, start_list: list):
        
        #mismatch error check
        if len(start_list) != self.samples:
            print(f"error need:{self.samples} samples, received:{start_list}")
            start_loc = tuple(start_list[0])
            self.start_loc_all(start_loc)
            return

        for sample_index, start_loc in enumerate(start_list):
            start_tuple = (start_loc[0], start_loc[1], self.start_time)
            self.data[sample_index, 0, start_tuple]
        print("individual intializations")
        self.curr_index = 0
   
    def get_num_samples(self):
        return self.data.shape[0]

    def get_length(self):
        return self.data.shape[1]

    def get_loc(self, time, sample):
        loc = self.data[sample, time, 0:2]
        return tuple(loc)

    def get_all_at_time(self, time):
        return self.data[:,time, 0:2]

    def set_loc(self, time, sample, loc):
        self.data[sample, time, :] = (loc[0], loc[1], time)

    def set_samples(self, num_samples):
        print("set_samples not finished")
        
    def set_length(self, length):
        print("set_samples not finished")


class HumanTravelModel(object):
    #TODO not adding time to the pathing yet will post process it based
    # on the length as the time indicator

    def __init__(self, data_proxy: GISproxy, model_layers=["depth", "trails"],
                 actions=((-1, 0), (0, 1), (0, -1), (1, 0), (0, 0))):
                 #north, east, west, south, stop

        self.tuple_actions = actions
        self.data_proxy = data_proxy

        self.depth_data,    \
        self.gradient_data, \
        self.trails_data =  self.load_maps(data_proxy, model_layers)

    def load_maps(self, data_proxy, model_layers):
        
        #TODO all or nothing approach to loading maps. consider dynamic
        # map loading and tansition model creation in future
        if "depth" in model_layers:
            depth_layer = data_proxy.get_layer("depth")
            print("loaded depth layer")
            depth_data = depth_layer["data"]
            gradient_data = self._depth_to_grad(depth_data)
            print("created gradient layer")
        else:
            print("error must add depth and gradient layer")

        if "trails" in model_layers:
            trails_layer = data_proxy.get_layer("trails")
            trails_data = trails_layer["data"]
            print("loaded trails layer")
        else:
            print("error must add trail layer")

        self._shape_check([depth_data, gradient_data, trails_data])

        return depth_data, gradient_data, trails_data

    def _depth_to_grad(self, depth_array):
        return np.gradient(depth_array, axis=-1)

    def _shape_check(self, data_arrays: list):
        
        check_list = []
        for data in data_arrays:
            check_list.append(data.shape)
        result = all(shape == check_list[0] for shape in check_list)
        print(f"do data arrays match? {result}")

    def rollout_path_obj(self, hiker_paths_obj: HikerPathsObj, 
                         time_horizon: int = 100):
        """
        """
        #Error check since PathObj currently not dynamic
        if time_horizon > hiker_paths_obj.get_length():
            print(f"ERROR path_objs size:{hiker_paths_obj.get_length()} \
            time_horizon size:{time_horizon}")
            return 

        actions = self.tuple_actions
        
        #reference dictionary for simpliflying transition func args
        environment = {"depth_data": self.depth_data,
                       "gradient_data": self.gradient_data,
                       "trails_data": self.trails_data}

        for time in tqdm(range(time_horizon-1)):
            for sample in range(hiker_paths_obj.get_num_samples()):

                loc = hiker_paths_obj.get_loc(time, sample)
                trans_loc = self.transition_func(loc, actions, environment)
                hiker_paths_obj.set_loc(time + 1, sample, trans_loc)
        
        hiker_paths_obj.curr_index = time_horizon

    def transition_func(self, loc, actions, environment: dict):
        
        depth = environment["depth_data"]
        gradient = environment["gradient_data"]
        trails = environment["trails_data"]

        action_scores = np.zeros(len(actions))

        action_scores = self._depth_score(loc, actions, \
                                          action_scores, depth)
        action_scores = self._gradient_score(loc, actions, \
                                             action_scores, gradient)
        action_scores = self._trail_score(loc, actions, \
                                          action_scores, trails)
        
        #normalize the actuion scores for transition model
        if action_scores.min() < 0:
            np.add(action_scores, -1*action_scores.min())
        trans_model =  [float(i)/sum(action_scores) for i in action_scores]
        
        
        bounds_check = False
        while bounds_check == False:
            #choose which action to take based on rand 
            rand_trans = np.random.rand()
            trans_density = 0
            for index, trans_prob in enumerate(trans_model):
                trans_density += trans_prob
                if rand_trans <= trans_density:
                    trans_loc = np.add(loc, actions[index])
                    break
            #hackey bounds check
            try:
                depth[trans_loc]
                bounds_check = True                
            except IndexError:
                print("hiker wants to leave the map") 
        
        return tuple(trans_loc)
    
    def _depth_score(self, loc: tuple, actions, action_scores, depth):
        
        curr_depth = depth[loc]
        for index, action in enumerate(actions):
            score = 0  
            action_depth = depth[tuple(np.add(action, loc))]
            #print(action_depth, curr_depth)
            if action_depth <= curr_depth:
                score = 20
            else: 
                score = 5
            action_scores[index] += score

        return action_scores 
            
    def _gradient_score(self, loc, actions, action_scores, gradient):
        
        for index, action in enumerate(actions):
            score = 0
            action_loc = tuple(np.add(action, loc))
            slope = gradient[action_loc]
            if slope >= 10:
                score = 0
            else:
                score = 5
            action_scores[index] += score

        return action_scores

    def _trail_score(self, loc, actions, action_scores, trails):
        
        for index, action in enumerate(actions):
            score = 0
            action_loc = tuple(np.add(action, loc))
            trail_avail = trails[action_loc]
            if trail_avail is True:
                score = 50
            action_scores[index] += score

        return action_scores

    def plot_gmm_depth(self, gmm, array_depth, sample_space):
        
        fig = plt.figure()
        
        x = np.linspace(0, 100, 20)
        y = np.linspace(0, 100, 20)

        X, Y = np.meshgrid(x, y)

        XX = np.array([X.ravel(), Y.ravel()]).T
        Z = gmm.score_samples(XX)
        Z = Z.reshape(X.shape)
        Z = np.exp(Z)
        #Z = np.add(Z, 10)
        #Z *= .1
        print(Z.shape)


        norm = plt.Normalize(Z.min(), Z.max())
        colors = cm.viridis(norm(Z))
        rcount, ccount, _ = colors.shape

        ax1 = fig.add_subplot(1, 3, 3, projection='3d')

        surf = ax1.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount,
                                facecolors=colors, shade=False)

        surf.set_facecolors((0, 0, 0, 0))
        #Z_dist_max = Z.max()*2
        
        xx, yy = np.meshgrid(np.linspace(0,100, 100), np.linspace(0,100, 100))
        X = xx 
        Y = yy
        Z = (xx * 0 )
        Z = np.subtract(Z, .00005)

        
        array_depth = np.subtract(array_depth, array_depth.min())
        array_depth = array_depth/array_depth.max()    # Uses 1 division and image.size multiplications


        ax1.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=plt.cm.copper(array_depth), shade=False)
        ax1.axis('off')
        #ax1.set_zlim(Z_dist_max)


        ax2 = fig.add_subplot(1, 3, 1)
        ax2.imshow(array_depth, cmap='copper')
        

        ax3 = fig.add_subplot(1, 3, 2)
        ax3.imshow(sample_space)

        plt.show()
