#!/usr/bin/python2
# -*- coding: utf-8 -*-

import subprocess,time,os
# stime = time.strftime('%Y%m%d%H%M%S',time.localtime())
work_dir = '/home/kilox/monitor'

# cnt = 0
# for f in os.listdir(work_dir):
#     name = int(os.path.split(f)[0]) +1
#     cnt = name%10
cnt = 0
cnt_file = os.path.join(work_dir,'cnt_file')
if os.path.exists(cnt_file):
    with open(cnt_file,'r') as f:
        cnt = int(f.readline()) + 1

with open(cnt_file,'w') as f:
    f.write('{} \n'.format(cnt))


os.chdir(work_dir)

write_name = os.path.join(work_dir,'{}.log'.format(cnt))
if os.path.exists('latest.log'):
    os.remove('latest.log')
if os.path.exists(write_name):
    os.remove(write_name)


while True:
    # logfile = '{}_{}.log'.format(stime,cnt)
    subprocess.Popen('./monitor.sh >> {}'.format(write_name),shell=True)
    time.sleep(60)
    subprocess.Popen('ln -s {} latest.log'.format(write_name),shell=True)
    