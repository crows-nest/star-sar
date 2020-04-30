
#! /usr/bin/python3

from particle_filter import PathParticleFilter, ObsPathObj
from human_motion import HumanTravelModel, HikerPathsObj
import numpy as np
from gis_proxy import GISproxy, open_json

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn import mixture
import matplotlib.image as mpimg
from sklearn.preprocessing import normalize


json_data = open_json('config_1.json')
data_proxy = GISproxy()
data_proxy.load_data(json_data["proxy_gis_filename"])

import scipy

import json

TOTAL_TIME = 1600
NUM_SAMPLES = 3000


from pomegranate import GeneralMixtureModel
from pomegranate import MultivariateGaussianDistribution, NormalDistribution


def linear_path(start_loc, end_loc):
    x_diff = end_loc[0] - start_loc[0]
    y_diff = end_loc[1] - start_loc[1]
    m = y_diff/x_diff
    b = start_loc[1] - m * start_loc[0]
    loc_list = [start_loc]
    for x in range(start_loc[0], end_loc[0]):
        y = int(m*x + b)
        loc_list.append((x, y))
    return loc_list

def pomegranate_to_scikitlearn(gmm_pom):
    data = json.loads(gmm_pom.to_json())

    n_components = len(data["distributions"])
    weights = data["weights"]
    clf = mixture.GaussianMixture(n_components=n_components, 
                                  weights_init=weights)
    means = []
    covs = []
    chol = []
    for dist in data["distributions"]:
        param_list = dist["parameters"]
        means.append(param_list[0])

        covs.append(param_list[1])
        chol.append(scipy.linalg.cholesky(param_list[1], lower=True))

    clf.means_ = np.asarray(means)
    clf.covariances_ = np.asarray(covs)
    clf.precisions_cholesky_ = np.asarray(chol)
    clf.weights_ = np.asarray(weights)
    
    return clf


start_loc_geo = (-105.2, 40.025)

depth_dict = data_proxy.gis_dict["depth"]
start_loc = data_proxy.get_pixel_coord(start_loc_geo, depth_dict)

#create hiker paths objecy
hiker_paths = HikerPathsObj(samples=NUM_SAMPLES, length=TOTAL_TIME)
hiker_paths.start_loc_all(start_loc)


human_model = HumanTravelModel(data_proxy)
human_model.rollout_path_obj(hiker_paths, time_horizon=TOTAL_TIME)



#obsevation objects
start_loc = (360, 90)
end_loc = (450, 90 )
loc_array = linear_path(start_loc, end_loc)
obs_path = ObsPathObj(length=TOTAL_TIME)
obs_path.load_loc_array(loc_array, 140)


#particle filtering weighting
p_filter = PathParticleFilter()
log_weights = p_filter.get_trail_obs_prob(hiker_paths, obs_path)


time_list = [100, 500, 900, 1500]
for time in time_list:
    samples = hiker_paths.get_all_at_time(time)

    weights = p_filter.weighting_func(log_weights)
    print(weights)
    print(samples) # NormalDistribution

    samples = [[float(item[0]),float(item[1])] for item in samples]

    test = np.random.multivariate_normal([50, 50], [[1, 0], [0, 1]], 10)


    print(test)


    gmm = GeneralMixtureModel.from_samples(MultivariateGaussianDistribution, 
                                        n_components=4, X=samples, 
                                        weights=weights)



    clf = pomegranate_to_scikitlearn(gmm)

    graph_shape = depth_dict["data"].shape
    print(graph_shape)


    # display predicted scores by the model as a contour plot

    ax = plt.subplot(111)

    x = np.linspace(0.0, graph_shape[0])
    y = np.linspace(0.0, graph_shape[1])
    X, Y = np.meshgrid(x, y)
    XX = np.array([X.ravel(), Y.ravel()]).T
    test = np.ones((2, 2))
    Z = -clf.score_samples(XX)
    Z = Z.reshape(X.shape)

    #norm = plt.Normalize(Z.min(), Z.max())
    cmap = plt.get_cmap('jet')


    #CS = ax.contour(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=1000.0),levels=np.logspace(0, 3, 10))

    surf = ax.contourf(X, Y, Z, alpha=.4, antialiased=True, cmap=cmap, 
                       norm=LogNorm(vmin=1.0, vmax=1000.0), 
                       levels=np.logspace(0, 3, 10))

    arr = mpimg.imread("../src/qt_ui/boulder.png")
    extent = ax.get_xlim()+ ax.get_ylim()
    ax.imshow(arr, extent=extent)

    plt.show()


"""
test = p_filter.sample_weight_at_time(human_model.array_path_objs, [obs_path], 100)

#print(test)

sample_list = []
for path_obj in human_model.array_path_objs:
    sample_list.append(path_obj.get_curr_loc())

print( )

data_proxy.plot_raster([sample_list])



"""
