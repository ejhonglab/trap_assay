#!/usr/bin/env python

"""
For the cameras that Kristina wants, this pushes their output through the ROS
tracking pipeline.
"""

from __future__ import print_function

import os
from os.path import join, split, exists, realpath, normpath
import subprocess as sp
import glob
import pprint

import yaml

if 'DATA_DIRS' not in os.environ:
    raw_data_dirs = [os.getcwd()]
else:
    raw_data_dirs = os.environ['DATA_DIRS']

for raw_data_dir in raw_data_dirs.split(':'):
    if len(raw_data_dir) == 0 or not exists(raw_data_dir):
        continue

    config_file = 'cam_purpose_config.yaml'
    # One of these needs to be defined.
    config_file_path = join(raw_data_dir, config_file)
    if not exists(config_file_path):
        print('First checked for config at {}'.format(config_file_path))
        config_file_path = join(split(split(realpath(__file__))[0])[0],
            config_file)

    print('Using config from {}'.format(config_file_path))
    with open(config_file_path, 'r') as f:
        data = yaml.load(f)

    avi_host2cams = data['to_make_avis']
    tracking_host2cams = data['to_track']

    # TODO delete after checking w/ K that new way is working
    '''
    tracking_host2cams = {
        'hong5': [0, 1],
        'walking': [0, 2, 5, 6]
    }
    '''

    glob_str = '*_*_*_*/'
    input_dirs = []
    for input_dir in glob.glob(join(raw_data_dir, glob_str)):
        input_dir = normpath(input_dir)
        last_part = split(input_dir)[1]
        parts = last_part.split('_')
        if len(parts) < 4:
            continue
        host = parts[0]
        try:
            cam_num = int(parts[-1])
        except ValueError:
            continue

        avi_host = host
        if avi_host not in avi_host2cams:
            avi_host = 'default'
        if cam_num in avi_host2cams[host]:
            cmds = ['rosrun', 'multi_tracker', 'bag2vid.py']
            p = sp.Popen(cmds, cwd=input_dir)
            p.communicate()

        if host not in tracking_host2cams:
            host = 'default'

        if cam_num in tracking_host2cams[host]:
            input_dirs.append(input_dir)

    input_dirs = sorted(input_dirs)

    all_dirs = [x[:-1] for x in glob.glob(join(raw_data_dir, '*/'))]
    excluded_dirs = sorted(list(set(all_dirs) - set(input_dirs)))

    print('Dirs to track:')
    pprint.pprint(input_dirs)
    print('\nExcluded dirs:')
    pprint.pprint(excluded_dirs)
    print('')

    # ROS bag file playback rate.
    # Higher = faster tracking and more computer load
    rate = 5.0
    for d in input_dirs:
        print('Tracking {}'.format(d))
        cmds = ['rosrun', 'multi_tracker', 'retrack_ros', d, str(rate)]
        # TODO maybe try to get progress somehow and send that to a progressbar
        # library, so we can suppress the ROS output? or just save ROS output to
        # a file anyway (doable?)?
        # TODO test all processes started are killed w/ ctrl-c
        p = sp.Popen(cmds)
        p.communicate()

