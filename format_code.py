#!/usr/bin/python3
import subprocess, os
import sys

# folder = '/home/kilox/slam_ws/src/ORB_SLAM2'

# folder = '/home/kilox/workspace/VINS-Course'
if len(sys.argv) > 1:
    folder = sys.argv[1]
    for root, dirs, files in os.walk(folder):
        for file in files:
            if 'build' in root or 'cmake-build-debug' in root:
                continue
            file_name = os.path.join(root, file)
            ext = os.path.splitext(file_name)[1]
            if ext in ['.cc', '.cpp', '.h']:
                subprocess.check_output('clang-format -style=file -i {}'.format(file_name), shell=True)
                print('process {}'.format(file_name))
else:
    print('use  ./format_code.py floder(which contain a .clang-format file)')
    # if file_name.endswith('.py'):
# /usr/bin/clang-format -style=file -i Optimizer.cc

# folder = '/home/kilox/workspace/VINS-Course'
# for root, dirs, files in os.walk(folder):
#     folder_name = os.path.dirname(root)
#     print(folder_name)
