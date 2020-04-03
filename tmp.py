import numpy as np

a = np.array([1, 2, 3, 4, 5, 6])
b = np.array([0, 2, 3, 1, 4])
# a = np.append([2],[1,2,3])
# print(a[b])
b = [2, 3, 4, 1, 5]
b = a[b]

print(b)


def test_pass_arg(a):
    a.append(1)
    return

a = []
#
test_pass_arg(a)
print(a)

a = np.arange(1,10)

# slice也是引用
b = a[1:5]
print(b)
b[2]= 100
print(a)

