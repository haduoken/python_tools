#!/usr/bin/python3

import os
import time
import subprocess
import shutil

script = os.path.join(os.getcwd(),'run.sh')

print(script)
if os.path.exists(script):
    print('hello world')

subprocess.run([script])
