import math


def dis(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2))


print(dis([-1.375915, -6.131201], [-1.410220, -6.113666]))

print(dis([-1.410220, -6.113666], [-1.434881, -6.117769]))
