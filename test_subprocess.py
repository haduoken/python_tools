import subprocess
import os
import time

print(time.strftime('%Y%m%d%H%M%S',time.localtime()))

subprocess.Popen('echo 1234 | sudo -S touch 1',shell=True).wait()
# proc = subprocess.Popen(['sudo','touch','1.txt']).wait()

# os.system('sudo ifconfig')
print(os.path.expanduser('~'))
# print('hello world')
# lines = [
#     '#!/bin/bash \n',
#     'sudo touch 1 \n',
# ]
# script_file = os.path.join(os.getcwd(), 'run.sh')
# with open(script_file, 'w') as f:
#     f.writelines(lines)
#     f.flush()
# os.system('chmod +x {}'.format(script_file))
# subprocess.Popen(script_file)