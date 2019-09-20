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
from pprint import pprint as pp

import yaml

debug = False
if 'DATA_DIRS' not in os.environ:
    raw_data_dirs = [os.getcwd()]
    print('Using current working directory as input since DATA_DIRS not set.')
else:
    raw_data_dirs = os.environ['DATA_DIRS']
    print('Using directories in DATA_DIRS for input')

# Matches on last part of raw_data_dir path and sends to a path relative to
# parent dir of raw_data_dir.
raw_data_dir2tracking_output_dir = {
    'original': 'retracked',
    'trap_assay': 'trap_assay_ROStracking',
}

for raw_data_dir in raw_data_dirs.split(':'):
    if debug:
        print('raw_data_dir:', raw_data_dir)

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
    if debug:
        print('config:', data)

    glob_str = '*_*_*_*/'
    input_dirs = []
    for input_dir in glob.glob(join(raw_data_dir, glob_str)):
        if debug:
            print('input_dir:', input_dir)

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

        if debug:
            print('cam_num', cam_num)
            print('host', host)

        avi_host = host
        if avi_host not in avi_host2cams:
            avi_host = 'default'

        if debug:
            print('for avi:')
            print(avi_host)
            print(avi_host2cams[avi_host])
            print(cam_num in avi_host2cams[avi_host])

        if cam_num in avi_host2cams[avi_host]:
            cmds = ['rosrun', 'multi_tracker', 'bag2vid.py']
            if debug:
                print('would try to make avi')
            else:
                p = sp.Popen(cmds, cwd=input_dir)
                p.communicate()

        if host not in tracking_host2cams:
            host = 'default'
        if cam_num in tracking_host2cams[host]:
            input_dirs.append(input_dir)

        if debug:
            print('for tracking:')
            print(host)
            print(cam_num in tracking_host2cams[host])
            print('')

    input_dirs = sorted(input_dirs)

    all_dirs = [x[:-1] for x in glob.glob(join(raw_data_dir, '*/'))]
    excluded_dirs = sorted(list(set(all_dirs) - set(input_dirs)))

    print('Dirs to track:')
    pprint.pprint(input_dirs)
    print('\nExcluded dirs:')
    pprint.pprint(excluded_dirs)
    print('')

    input_parent, input_pathend = split(normpath(raw_data_dir))
    output_pathend = raw_data_dir2tracking_output_dir[input_pathend]
    retracking_dir = join(input_parent, output_pathend)
    print('Using {} as retracking dir'.format(retracking_dir))

    # ROS bag file playback rate.
    # Higher = faster tracking and more computer load
    rate = 5.0
    for d in input_dirs:
        print('Tracking {}'.format(d))
        cmds = ['rosrun', 'multi_tracker', 'retrack_ros', d, retracking_dir,
            str(rate)]

        # TODO maybe try to get progress somehow and send that to a progressbar
        # library, so we can suppress the ROS output? or just save ROS output to
        # a file anyway (doable?)?
        # TODO test all processes started are killed w/ ctrl-c
        if debug:
            print('would try to track')
        else:
            p = sp.Popen(cmds)
            p.communicate()

