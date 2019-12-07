from numpy.linalg import norm
from numpy import arccos, array, dot, pi, cross
import math
import numpy as np

p1 = np.array([1, 2])
p2 = np.array([0, 0])
p3 = np.array([3, 3])





# d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
# print(d)
# print(3 / math.sqrt(5))

print(distance_numpy(p1,p2,p3))
