#!/usr/bin/env python

"""
For the cameras that Kristina wants, this pushes their output through the ROS
tracking pipeline.
"""

from __future__ import print_function

import os
from os.path import join, exists
import subprocess as sp
import glob
import pprint

raw_data_dir = join(os.environ['DATA_DIR'], 'original')

host2cams = {
    'hong5': [0, 1],
    'walking': [0, 2, 5, 6]
}
input_dirs = []
for host, cams in host2cams.items():
    for cam in cams:
        glob_str = '{}_*_{}'.format(host, cam)
        input_dirs.extend(glob.glob(join(raw_data_dir, glob_str)))
input_dirs = sorted(input_dirs)

all_dirs = [x[:-1] for x in glob.glob(join(raw_data_dir, '*/'))]
excluded_dirs = sorted(list(set(all_dirs) - set(input_dirs)))

print('Dirs to track:')
pprint.pprint(input_dirs)
print('\nExcluded dirs:')
pprint.pprint(excluded_dirs)
print('')

# ROS bag file playback rate. Higher = faster tracking and more computer load
rate = 5.0
for d in input_dirs:
    print('Tracking {}'.format(d))
    cmds = ['rosrun', 'multi_tracker', 'retrack_ros', d, str(rate)]
    # TODO maybe try to get progress somehow and send that to a progressbar
    # library, so we can suppress the ROS output? or just save ROS output to a
    # file anyway (doable?)?
    # TODO test all processes started are killed w/ ctrl-c
    p = sp.Popen(cmds)
    p.communicate()

