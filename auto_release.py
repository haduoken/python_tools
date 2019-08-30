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

# 编译项目
os.chdir(os.path.join(catkin_ws_name,'src'))
# subprocess.Popen('git clone ssh://git@172.16.2.5:30001/Mxw/kilox_navigation.git --depth 1',shell=True).wait()
# subprocess.Popen('git clone ssh://git@172.16.2.5:30001/KiloX/kilox_robot.git --depth 1',shell=True).wait()
subprocess.Popen('git clone ssh://git@172.16.2.5:30001/KiloX/kilox_pantilt.git --depth 1',shell=True).wait()
os.chdir(os.path.join(catkin_ws_name))
subprocess.Popen('catkin_make install',shell=True).wait()

# 将需要的shell脚本拷贝过去
for file in os.listdir(devel_dir):
    if os.path.splitext(file)[1]=='sh' or os.path.splitext(file)[1]=='bash':
        shutil.copy(file,install_dir)

# 将install文件件打包成KiloXImage_xxx.tar.gz, 并存放在工作目录
img_name = 'KiloXImage_{}.tar.gz'.format(str_time)
os.chdir(ws)
subprocess.Popen('tar -cf {} {}'.format(img_name,os.path.relpath(install_dir,os.getcwd())),shell=True).wait()

# 删除掉临时的编译工作空间
shutil.rmtree(catkin_ws_name)

