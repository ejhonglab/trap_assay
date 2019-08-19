#!/usr/bin/env bash

# TODO use wget instead of curl. in multi_tracker install scripts + trap_assay one liner
curl -s https://raw.githubusercontent.com/tom-f-oconnell/multi_tracker/master/setup/install.sh | bash

cd ~/catkin/src
git clone https://github.com/tom-f-oconnell/metatools
git clone https://github.com/tom-f-oconnell/usb_cam
git clone https://github.com/ejhonglab/trap_assay
cd ~/catkin
source /opt/ros/kinetic/setup.bash
catkin_make

mkdir ~/experiments
cp ~/catkin/src/trap_assay/example_config/*.yaml ~/experiments/
cp ~/catkin/src/trap_assay/example_config/*.py ~/experiments/
echo "You may need to change settings in YAML files under ~/experiments"

echo "alias roslaunch='ROS_HOME=\`pwd\` roslaunch'" >> ~/.bash_aliases
echo "alias transfer_data='rsync -avPuz $HOME/experiments/ lab@cthulhu:/mnt/tb/original'" >> ~/.bash_aliases

