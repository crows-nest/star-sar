#! /usr/bin/python3

import os
import copy

import matplotlib.pyplot as plt
from GIS_proxy import GIS_proxy, open_json
import numpy as np
from tqdm import tqdm
from sklearn import mixture
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


class human_motion_model(object):

    # north, east, west, south, stop
    tuple_actions = ((-1, 0), (0, 1), (0, -1), (1, 0), (0, 0))

    def execute_mcmc(self, data_proxy, list_layers=["depth", "trails"],
                   num_samples=10, time_steps=10, geo_loc=(-105.30, 40.05)):

        self.data_proxy = data_proxy
        
        if "depth" in list_layers:
            depth_layer = data_proxy.get_layer("depth")
            print("loaded depth layer")
            depth_data = depth_layer["data"]
            gradient_data = self.depth_to_grad(depth_data)

        if "trails" in list_layers:
            trails_layer = data_proxy.get_layer("trails")
            trails_data = trails_layer["data"]
            print("loaded trails layer")
        
        sample_space = np.zeros(depth_layer["data"].shape)
        index_loc = data_proxy.get_pixel_coord(geo_loc, depth_layer)


        for i in tqdm(range(num_samples)):

            sample_loc = self.sample_rollout(index_loc, time_steps,
                                             depth_data, 
                                             gradient_data, 
                                             trails_data)

            sample_space[sample_loc[0], sample_loc[1]] += 1

        return sample_space

    def sample_rollout(self, location, time_steps, depth, gradient, trails):

        max_values = depth.shape
        #curr_loc = location
        curr_loc = (300, 200)
        i = 0
        while i <= time_steps:
            rand_trans = np.random.rand()

            actions = self.tuple_actions
            action_scores = np.zeros(len(actions))
            #bias
            action_scores[1] = 20
            action_scores[4] = -20

            action_scores = self.depth_score(curr_loc, actions, 
                                            action_scores, depth)
            action_scores = self.gradient_score(curr_loc, actions, 
                                                action_scores, gradient)
            action_scores = self.trail_score(curr_loc, actions, 
                                             action_scores, trails)
            
            #normalize the actuion scores for transition model
            if action_scores.min() < 0:
                np.add(action_scores, -1*action_scores.min())
            trans_model =  [float(i)/sum(action_scores) for i in action_scores]

            #choose which action to take based on rand transition
            trans_density = 0
            for index, trans_prob in enumerate(trans_model):
                trans_density += trans_prob
                if rand_trans <= trans_density:
                    prop_loc = np.add(curr_loc, actions[index])
                    break

            #TODO an out of bounds check
            curr_loc = tuple(prop_loc)
            i += 1

        return curr_loc

    def depth_score(self, loc, actions, action_scores, depth):
        
        curr_depth = depth[loc]
        for index, action in enumerate(actions):
            score = 0    
            action_depth = depth[tuple(np.add(action, loc))]
            if action_depth <= curr_depth:
                score = 20
            else: 
                score = 5
            action_scores[index] += score

        return action_scores 
            
    def gradient_score(self, loc, actions, action_scores, gradient):
        
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

    def trail_score(self, loc, actions, action_scores, trails):
        
        for index, action in enumerate(actions):
            score = 0
            action_loc = tuple(np.add(action, loc))
            trail_avail = trails[action_loc]
            if trail_avail is True:
                score = 50
            action_scores[index] += score

        return action_scores

    def gmm_from_samples(self, sample_space):

        sample_list = self._sample_space_to_samples(sample_space)
        gmm = mixture.GaussianMixture(n_components=10).fit(sample_list)
        
        print(gmm.means_)
        return gmm

    def _sample_space_to_samples(self, sample_space):
        sample_list = []

        for i in range(len(sample_space)):
            for j in range(len(sample_space[0])):
                num_samples = sample_space[i][j]
                for hit in range(int(num_samples)):
                    sample_list.append((j,i))

        return sample_list    

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
        pass

    def depth_to_grad(self, depth_array):

        return np.gradient(depth_array, axis=-1)