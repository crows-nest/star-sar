#! /usr/bin/python3

import os

import matplotlib.pyplot as plt
from crow_gis.GIS_topo import GIS_topo
import numpy as np
from tqdm import tqdm
from sklearn import mixture
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


GIS_ENABLE = 1
TRANSITION_ORDER = ["left", "forward", "right", "backward", "stop"]


def markov_chain_monte_carlo(state_space, 
                             num_samples=10, time_steps=2):

    sample_space = np.zeros(state_space.shape)
    print(sample_space.shape)

    for i in tqdm(range(num_samples)):
        location = sampled_location(state_space, time_steps)
        sample_space[location[0], location[1]] += 1
    return sample_space

def sampled_location(state_space, time_steps):
    
    index = [60, 5]
    max_values = state_space.shape

    model_sum = lambda model, index: sum(model[0:index+1])

    transition_sums = [0.0, 0.0, 0.0, 0.0, 0.0]
    i = 0
    while i <= time_steps:
        rand_transition = np.random.rand()

        array_grad = depth_to_grad(state_space)
        array_grad_local = get_neighbor_gradients(np.asarray(array_grad[0]), index)
        #array_grad = get_neighbor_gradients(state_space, index)
        dict_transition_model = depth_trans_model(array_grad_local, index)

        transition_model = []
        for direction in TRANSITION_ORDER:
            value = dict_transition_model[direction]
            transition_model.append(value)

        #TODO how do  I fix this garbagio?
        if rand_transition <= model_sum(transition_model, 0): #move left
            #print(f"rand {transition} move left")
            index[0] += 1

            if index[0] < 0 or index[0] >= max_values[0]:
                index[0] -= 1
                continue
            else:
                i += 1
                transition_sums[0] += 1
            
        elif rand_transition <= model_sum(transition_model, 1):
            #print(f"rand {transition} move forward")
            index[1] += 1
            if index[1] < 0 or index[1] >= max_values[1]:
                index[1] -= 1
                continue
            transition_sums[1] += 1

        elif rand_transition <= model_sum(transition_model, 2):
            #print(f"rand {transition} move right")
            index[0] -= 1
            if index[0] < 0 or index[0] >= max_values[0]:
                index[0] += 1
                continue
            else:
                i += 1
                transition_sums[2] += 1


        elif rand_transition <= model_sum(transition_model, 3):
            #print(f"rand {transition} move backward")
            index[1] -= 1
            if index[0] < 0 or index[0] >= max_values[0]:
                index[1] += 1
                continue
            else:
                i += 1
                transition_sums[3] += 1

        elif rand_transition <= model_sum(transition_model, 4):
            #print(f"rand {transition} stop")
            i += 1
            transition_sums[4] += 1
        
    total_sum = sum(transition_sums)
    probabilites = [x / total_sum for x in transition_sums]
    #print(probabilites)
    return index

def depth_trans_model(array_grad, index):
    dict_movement = {"forward": (1, 2), "left": (0, 1), "right": (2, 1), 
                      "backward": (1, 0), "stop":(1, 1) }

    dict_transition_model = {"forward": 20 , "left": 10, "right": 10, 
                             "backward": 0, "stop": 5 }

    sum_score =  0
    for key in dict_movement:
        index = dict_movement[key]
        gradient = array_grad[index[0],index[1]]
        grad_score = gradient_score(gradient)
        dict_transition_model[key] += grad_score
        sum_score +=  dict_transition_model[key]

    for transition in dict_transition_model:
        dict_transition_model[transition] /= sum_score
        
    return dict_transition_model

def gradient_score(gradient):

    #TODO maybe build a better transition model from this?
    if gradient < 0:
        return 15

    else:
        return 5

def get_neighbor_gradients(array_grad, loc):

    array_grad_local = array_grad[loc[0]-1:loc[0]+2:, loc[1]-1:loc[1]+2:]
    
    return array_grad_local

def get_neighbor_gradients_old(state_space, loc):
    
    array_indexing = [-1, 0, 1]
    height_loc = state_space[loc[0], loc[1]]
    array_grad = np.zeros((3, 3))
    #TODO not checking for edge of map
    for index_i, i in enumerate(array_indexing):
        for index_j, j in enumerate(array_indexing):
            x = loc[0] + i
            y = loc[1] + j
            
            height_neighbor = state_space[x, y]
            grad = height_neighbor - height_loc
            array_grad[index_i, index_j] = grad
    
    return array_grad

def gmm_from_samples(sample_space):

    sample_list = sample_space_to_samples(sample_space)
    gmm = mixture.GaussianMixture(n_components=10).fit(sample_list)
    
    print(gmm.means_)
    return gmm

def sample_space_to_samples(sample_space):
    sample_list = []

    for i in range(len(sample_space)):
        for j in range(len(sample_space[0])):
            num_samples = sample_space[i][j]
            for hit in range(int(num_samples)):
                sample_list.append((j,i))

    return sample_list    

def plot_gmm_depth(gmm, array_depth, sample_space):
    
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

def depth_to_grad(depth_array):

    return np.gradient(depth_array)


if __name__ == "__main__":


    if GIS_ENABLE:
        GIS_obj = GIS_topo()
        
       
        src_ds = GIS_obj.open_geotiff(GIS_obj.filename)
        array_depth = GIS_obj.get_depth_np(src_ds)

        mini_array = array_depth[1000:1100, 1000:1100]
        print(mini_array.shape)
     
        sample_space = markov_chain_monte_carlo(mini_array, 
                                                   num_samples = 1000, 
                                                   time_steps = 80)
        
        sample_gmm = gmm_from_samples(sample_space)
        
        differential_grid = depth_to_grad(mini_array)

        plot_gmm_depth(sample_gmm, mini_array, sample_space)

        
        #fig, ax = plt.subplots()
        #ax.imshow()

    
    
    else:
        array_depth = np.zeros((100,100))
        array_MC = np.zeros(array_depth.shape)


        transition_model_desc = ["left", "forward", "right", "backward", "stop"]
        transition_model = [0.1, 0.4, 0.1, 0.0, 0.4]
        posterior_array = markov_chain_monte_carlo(array_MC,
                                                   num_samples= 10, 
                                                   time_steps= 100)

        plt.imshow(posterior_array)
        plt.show()
