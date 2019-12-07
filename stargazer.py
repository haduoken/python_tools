#!/usr/bin/python3
# coding=utf-8

import os
import sys
import argparse
import shutil
import time
import subprocess

# 支持多个git项目的同时管理
# status xxx.tar.gz is [not] running
# start xxx.tar.gz is running not running. starting
# stop xxx.tar.gz is running. stopping
# restart xxx.tar.gz ...

# 传入xxx.tar.gz

# 关闭动作关闭相关的launch程序,以及杀掉node,
# 将log记录到文件
# 增加status, 可以查看版本,以及运行状态
# 打印当前使用版本
parser = argparse.ArgumentParser(description='none')
parser.add_argument('cmd', help='user command [start stop]')
args = parser.parse_args()

stargazer_dir = os.getcwd()


# 搜索已有的包, 然后提供用户选择使用哪一个

# /base_link_to_laser
# /chassis_configure_server
# /joy_xbox
# /kilox_global_plan_service
# /kilox_joint_state_pub
# /kilox_joy_controller
# /kilox_modbus_tcp_fast_node
# /kilox_modbus_tcp_node
# /kilox_move_to_pose_from_rviz_client
# /kilox_navigation_show_node
# /kilox_robot_control_p2r3_plc
# /kilox_robot_manager
# /kilox_sub_e_stop_call_cancel_task
# /laser_nodelet_manager
# /laser_nodelet_manager_cloud
# /laser_nodelet_manager_driver
# /laser_nodelet_manager_laserscan
# /localization_service
# /mapping_service
# /robot_state_publisher
# /rosout
# /tf2_web_republisher
def try_stop_one(name):
    try:
        ret = subprocess.check_output('rosnode list | grep {}'.format(name), shell=True)
        ret = ret.decode('utf-8')
        print(ret)
        if name in ret:
            print('关闭{}, 关闭中...'.format(name))
            subprocess.Popen('rosnode kill {}'.format(name), shell=True).wait()
    except subprocess.CalledProcessError:
        pass


def try_stop():
    try_stop_one('camera_node')
    try_stop_one('base_link_to_laser')
    try_stop_one('chassis_configure_server')
    try_stop_one('joy_xbox')
    try_stop_one('kilox_global_plan_service')
    try_stop_one('kilox_joint_state_pub')
    try_stop_one('kilox_joy_controller')
    try_stop_one('kilox_modbus_tcp_fast_node')
    try_stop_one('kilox_modbus_tcp_node')
    try_stop_one('kilox_move_to_pose_from_rviz_client')
    try_stop_one('kilox_navigation_show_node')
    try_stop_one('kilox_sub_e_stop_call_cancel_task')
    try_stop_one('kilox_robot_control_p2r3_plc')
    try_stop_one('kilox_robot_manager')
    try_stop_one('laser_nodelet_manager')
    try_stop_one('laser_nodelet_manager_cloud')
    try_stop_one('laser_nodelet_manager_laserscan')
    try_stop_one('localization_service')
    try_stop_one('mapping_service')
    try_stop_one('robot_state_publisher')
    try_stop_one('tf2_web_republisher')
    
    # 如果有roslaunch也关闭
    ret = subprocess.Popen("ps aux|grep new_robot_run.launch |grep -v grep | awk '{print $2}'|xargs kill -9",
                           shell=True)

    print('程序已经关闭')


def try_start():
    already_have = []
    for file in os.listdir(stargazer_dir):
        if os.path.splitext(file)[1] == '.gz':
            already_have.append(file)
    
    print("* 选择一个执行 *")
    for cur, file in enumerate(already_have):
        print('[{}]  {}'.format(cur, file))
    number = int(input())
    
    package_name = None
    if number < len(already_have):
        package_name = already_have[number]
    
    if package_name is None:
        print('没有合适的包')
        return
    
    # 如果不存在文件夹则进行解压文件, 删除log
    extracted = os.path.splitext(os.path.splitext(os.path.basename(package_name))[0])[0]
    extracted_path = os.path.join(os.getcwd(), extracted)
    if not os.path.exists(extracted_path):
        os.makedirs(extracted_path)
    img_file = os.path.abspath(package_name)
    subprocess.Popen('tar -xf {}'.format(img_file), shell=True).wait()
    log_file = os.path.join(stargazer_dir, '{}.log'.format(extracted))
    if os.path.exists(log_file):
        os.remove(log_file)
    # 修改bashrc文件里面的source的东西
    bash_file = os.path.join(extracted_path, 'setup.bash')
    cmd = 'source {} '.format(bash_file)
    subprocess.Popen("sed -i '/{}/d' ~/.bashrc".format('Stargazer'),
                     shell=True).wait()
    subprocess.Popen("echo '{}' >> ~/.bashrc".format(cmd), shell=True)
    # 运行命令
    lines = [
        '#!/bin/bash \n',
        'source {} \n'.format(bash_file),
        'cd {} \n'.format(stargazer_dir),
        'nohup roslaunch kilox_robot_manager new_robot_run.launch >> {} 2>&1&\n'.format(
            log_file),
    ]
    script_file = os.path.join(extracted_path, 'run.sh')
    with open(script_file, 'w') as f:
        f.writelines(lines)
        f.flush()
    os.system('chmod +x {}'.format(script_file))
    subprocess.Popen(script_file)
    print('success :)')


if __name__ == '__main__':
    print('use with [start | stop | restart ] ')
    cmd = args.cmd
    if cmd == 'stop' or cmd == 'restart' or cmd == 'start':
        print('尝试先关闭已运行程序')
        try_stop()
    if cmd == 'start' or cmd == 'restart':
        try_start()

