#!/usr/bin/env bash

# TODO use wget instead of curl. in multi_tracker install scripts + trap_assay one liner
curl -s https://raw.githubusercontent.com/tom-f-oconnell/multi_tracker/master/setup/install.sh | bash
if [ $? -eq 0 ]; then
    echo "multi_tracker installed successfully"
else
    echo "multi_tracker install failed! exiting!"
    exit 1
fi

# Otherwise setting focus won't work right for the cameras.
sudo apt install v4l-utils

cd ~/catkin/src
git clone https://github.com/tom-f-oconnell/metatools
git clone https://github.com/tom-f-oconnell/usb_cam
git clone https://github.com/ejhonglab/trap_assay
cd ~/catkin

# Otherwise some rosdep install will fail on fresh systems without pip.
sudo apt-get install python-pip -y

source /opt/ros/kinetic/setup.bash
# this one might not be necessary
source ~/catkin/devel/setup.bash
rosdep install -y metatools
if [ $? -eq 0 ]; then
    echo "metatools dependencies installed successfully"
else
    echo "metatools dependencies were NOT installed successfully. exiting!"
    exit 1
fi

catkin_make

mkdir ~/experiments
cp ~/catkin/src/trap_assay/example_config/*.yaml ~/experiments/
cp ~/catkin/src/trap_assay/example_config/*.py ~/experiments/
echo "You may need to change settings in YAML files under ~/experiments"

echo "alias roslaunch='ROS_HOME=\`pwd\` roslaunch'" >> ~/.bash_aliases
echo "alias transfer_data='rsync -avPuz $HOME/experiments/ lab@cthulhu:/mnt/tb/original'" >> ~/.bash_aliases

