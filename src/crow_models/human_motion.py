#! /usr/bin/python3

import os

import matplotlib.pyplot as plt
from crow_gis.GIS_topo import GIS_topo
import numpy as np

GIS_ENABLE = 1


def markov_chain_monte_carlo(state_space, transition_model, 
                             num_samples=1000, time_steps=20):

    sample_space = np.zeros(state_space.size)

    for i in range(num_samples):

        location = sampled_location(state_space, transition_model, time_steps)

        state_space[location[0], location[1]] += 1
        

    return state_space


def sampled_location(state_space, transition_model, time_steps):
    
    index = [50, 5]
    max_values = state_space.shape

    model_sum = lambda model, index: sum(model[0:index+1])

    transition_sums = [0.0, 0.0, 0.0, 0.0, 0.0]
    i = 0
    while i <= time_steps:
        transition = np.random.rand()

        if transition <= model_sum(transition_model, 0): #move left
            #print(f"rand {transition} move left")
            index[0] += 1

            if index[0] < 0 or index[0] >= max_values[0]:
                index[0] -= 1
                continue

            else:
                i += 1
                transition_sums[0] += 1
            

        elif transition <= model_sum(transition_model, 1):
            #print(f"rand {transition} move forward")
            index[1] += 1
            if index[1] < 0 or index[1] >= max_values[1]:
                index[1] -= 1
                continue

            transition_sums[1] += 1

        elif transition <= model_sum(transition_model, 2):
            #print(f"rand {transition} move right")
            index[0] -= 1
            if index[0] < 0 or index[0] >= max_values[0]:
                index[0] += 1
                continue
             
            else:
                i += 1
                transition_sums[2] += 1


        elif transition <= model_sum(transition_model, 3):
            #print(f"rand {transition} move backward")
            index[1] -= 1
            if index[0] < 0 or index[0] >= max_values[0]:
                index[1] += 1
                continue
            else:
                i += 1
                transition_sums[3] += 1

        elif transition <= model_sum(transition_model, 4):
            #print(f"rand {transition} stop")
            i += 1
            transition_sums[4] += 1
        



    total_sum = sum(transition_sums)
    probabilites = [x/ total_sum for x in transition_sums]
    #print(probabilites)


    return index


def depth_trans_model(array_grad):
    dict_movement = {"forward": (1, 2), "left": (0, 1), "right": (2, 1), 
                      "backward": (1, 0), "stop":(1, 1) }


    dict_transition_model = {"forward": 4 , "left": 2, "right": 2, 
                             "backward": 0, "stop": 4 }

    sum_score =  0
    for key in dict_movement:
        index = dict_movement[key]
        gradient = array_grad[index[0],index[1]]
        score = gradient_score(gradient)
        dict_transition_model[key] += score
        sum_score +=  dict_transition_model[key]


    for transition in dict_transition_model:
        dict_transition_model[transition] /= sum_score
        

    print(dict_transition_model)
    pass

def gradient_score(gradient):

    if -10 <= gradient <= 10:
        return 20

    else:
        return 10


def get_neighbor_gradients(state_space, loc):
    
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




if __name__ == "__main__":


    if GIS_ENABLE:
        GIS_obj = GIS_topo()
        
        dir_path = dirname = os.path.dirname(os.path.realpath(__file__))

        dir_path = dir_path.split("crow_models")[0]
        filename = os.path.join(dir_path, 'crow_gis/n40_w106_1arc_v3.tif')

        src_ds = GIS_obj.open_geotiff(filename)
        array_depth = GIS_obj.extract_depth_np(src_ds)

        mini_array = array_depth[1000:1100, 1000:1100]

        array_grad = get_neighbor_gradients(mini_array, (50, 50))

        print(depth_trans_model(array_grad))



        #plt.imshow(array_depth[1000:1100, 1000:1100])
        #plt.show()


    
    else:
        array_depth = np.zeros((100,100))
        array_MC = np.zeros(array_depth.shape)


        transition_model_desc = ["left", "forward", "right", "backward", "stop"]
        transition_model = [0.1, 0.4, 0.1, 0.0, 0.4]
        posterior_array = markov_chain_monte_carlo(array_MC, transition_model,
                                                num_samples= 100, time_steps= 50)

        plt.imshow(posterior_array)
        plt.show()
