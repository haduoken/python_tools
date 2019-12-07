#!/usr/bin/python3
# coding=utf-8
import os
import time
import subprocess
import shutil
import sys

# 可以指定远端分支进行编译
# 编译好的名称要涵盖版本信息
# 每一个git项目应该被编译成一个tar.gz

branch_name = 'dev'
repo_name = 'Stargazer'
if len(sys.argv) > 1:
    branch_name = sys.argv[1]

# 得到当前的工作空间, 也就是执行python脚本的地方
ws = os.getcwd()
# 新建catkin_ws, catkin_ws的唯一名字为时间字符串
str_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
catkin_ws_name = 'tmp_{}'.format(str_time)
catkin_ws_name = os.path.join(ws, catkin_ws_name)
os.makedirs(os.path.join(catkin_ws_name, 'src'))
src_dir = os.path.join(catkin_ws_name, 'src')
devel_dir = os.path.join(catkin_ws_name, 'devel')
install_dir = os.path.join(catkin_ws_name, 'install')

# 编译项目
os.chdir(os.path.join(catkin_ws_name, 'src'))
# subprocess.Popen('git clone ssh://git@172.16.2.5:30001/Mxw/kilox_navigation.git --depth 1',shell=True).wait()
# subprocess.Popen('git clone ssh://git@172.16.2.5:30001/KiloX/kilox_robot.git --depth 1',shell=True).wait()
subprocess.Popen('git clone ssh://git@172.16.2.5:30001/Robotics/Stargazer.git', shell=True).wait()
os.chdir(os.path.join(src_dir, repo_name))
subprocess.Popen('git checkout {}'.format(branch_name), shell=True).wait()
os.chdir(catkin_ws_name)
subprocess.Popen('catkin_make install -j4', shell=True).wait()

# 将需要的shell脚本拷贝过去
for file in os.listdir(devel_dir):
    ext = os.path.splitext(file)[1]
    if ext == 'sh' or ext == 'bash' or ext == 'zsh':
        shutil.copy(file, install_dir)

# 将版本信息写进去

# 将install文件件打包成KiloXImage_xxx.tar.gz, 并存放在工作目录
img_pure_name = '{}_{}_{}'.format(str_time, repo_name,branch_name)
img_name = '{}.tar.gz'.format(img_pure_name)
# os.chdir(ws)
os.chdir(catkin_ws_name)
shutil.move(install_dir, img_pure_name)
subprocess.Popen("tar -cf '{}' {}".format(img_name, img_pure_name), shell=True).wait()
shutil.move(img_name, ws)

# 删除掉临时的编译工作空间
shutil.rmtree(catkin_ws_name)
