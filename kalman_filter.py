import numpy as np
import matplotlib.pyplot as plt




estimate_x = np.zeros((6, 11))
prior_estimate_x = np.zeros(11)
estimate_x[0] = 10
True_value = np.array([None, 50.479, 51.025, 51.5, 52.003, 52.494, 53.002, 53.499, 54.006, 54.498, 54.991])
P = np.zeros(11)
K = np.zeros(11)
Z = np.array([None, 50.45, 50.967, 51.6, 52.106, 52.492, 52.819, 53.433, 54.007, 54.523, 54.99])
P[0] = 10000
T = np.arange(0, 11)
# 这里我们自信地觉得我们的模型是正确的, 于是将process noise 设置为很小
Q = 0.0001
R = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
for t in T[1:]:
    prior_estimate_x[t] = estimate_x[t - 1]
    P[t] = P[t - 1] + Q
    
    K[t] = P[t] / (P[t] + R[t])
    
    estimate_x[t] = prior_estimate_x[t] + K[t] * (Z[t] - prior_estimate_x[t])
    P[t] = (1 - K[t]) * P[t]

plt.figure()
plt.plot(T[1:], estimate_x[1:], label='estimate')
plt.plot(T[1:], Z[1:], label='measurement')
plt.plot(T[1:], True_value[1:], label='True value')
plt.legend()
