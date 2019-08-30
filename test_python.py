#!/usr/bin/python3

import os
import time
import subprocess
import shutil

# 得到当前的工作空间, 也就是执行python脚本的地方
ws = os.getcwd()
# 新建catkin_ws, catkin_ws的唯一名字为时间字符串
str_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
catkin_ws_name = 'tmp_{}'.format(str_time)
catkin_ws_name = os.path.join(ws,catkin_ws_name)
os.makedirs(os.path.join(catkin_ws_name,'src'))
src_dir = os.path.join(catkin_ws_name,'src')
devel_dir = os.path.join(catkin_ws_name,'devel')
install_dir = os.path.join(catkin_ws_name,'install')

print(os.path.relpath(install_dir,ws))