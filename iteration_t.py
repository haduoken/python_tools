import numpy as np
import matplotlib.pyplot as plt
import math

# y = 3x^3 + 2x^2 + x + 5

x = np.arange(1, 100)

# y = x ** 3 - 15 * x ** 2 + 500 * x + 5

y1 = 3 * x ** 2 - 30 * x + 500

print(y1)
plt.figure()
plt.plot(x, y1)
plt.show()
