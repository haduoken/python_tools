#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess

ret = subprocess.Popen(
    'roslaunch rs_localization rs_localization.launch map:={}  >>{} 2>&1& '.format('map',
                                                                                   'localization.log'),shell=True).wait()
print(ret)