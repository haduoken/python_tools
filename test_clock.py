import subprocess
import os



# lines = [
#     '#!/bin/bash \n',
#     'source /opt/ros/kinetic/setup.bash \n',
#     'rosparam get /run_id \n',
# ]
# script_file = os.path.join('/home/kilox/run1.sh')
# with open(script_file, 'w') as f:
#     f.writelines(lines)
#     f.flush()
# os.system('chmod +x {}'.format(script_file))
run_id = subprocess.check_output('#!/bin/bash;source /opt/ros/kinetic/setup.zsh;rosparam get /run_id',shell=True)
run_id = run_id.decode('utf-8')

print(run_id)
