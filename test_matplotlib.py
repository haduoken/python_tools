#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

# 如何使用动画的形式, 展示出数据
fig, ax = plt.subplots()
x = np.arange(0, 2 * np.pi, 0.01)
line, = ax.plot(x, np.sin(x))


# 第i帧
def animate(i):
    line.set_ydata(np.sin(x + i / 100))
    return line,


# 定义
def init():
    line.set_ydata(np.sin(x))
    return line,


# 如何产生动画? frames的总共长度, interval 是更新间隔, blit 是否更新整张图片
ani = animation.FuncAnimation(fig=fig, func=animate, frames=100, init_func=init, interval=200, blit=False)
plt.show()

ani.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])