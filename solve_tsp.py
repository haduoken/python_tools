import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
import math

num_points = 50

robot_pose = [0.2, 0.2]
points_coordinate = np.random.rand(num_points, 2)  # generate coordinate of points
distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')


# print(points_coordinate)

def get_dis(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    # print(routine)
    num_points, = routine.shape
    dis = sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])
    
    first_task = points_coordinate[routine[0]]
    dis += get_dis(first_task, robot_pose)
    
    return dis


# %% do GA

from sko.GA import GA_TSP


def solve():
    ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=50, max_iter=500, prob_mut=1)
    best_points, best_distance = ga_tsp.run()
    
    # %% plot
    fig, ax = plt.subplots(1, 2)
    
    best_points_ = np.concatenate([best_points, [best_points[0]]])
    best_points_coordinate = points_coordinate[best_points_, :]
    print(best_points_coordinate)
    print(get_dis(best_points_coordinate[0], robot_pose))
    ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
    ax[1].plot(ga_tsp.generation_best_Y)
    plt.show()


solve()
