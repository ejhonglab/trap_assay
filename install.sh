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

# To make it easier to administer the acquisition node later.
sudo apt install openssh-server

# All steps necessary to setup acquisition direct to the NAS, apart from:
# - adding mount point in fstab
sudo apt install openvpn nfs-common
sudo mkdir /mnt/nas
sudo chmod 777 /mnt/nas
# This link will be broken until mount point is setup
# TODO that ok? (didn't seem to work as part of vagrant setup, but did when
# pasting into vagrant shell...)
ln -s /mnt/nas/Kristina/direct2nas_experiments $HOME/nas_experiments
sudo su -c "echo '# Uncomment line below to allow NAS access on boot' >> /etc/fstab"
sudo su -c "echo '#storage:/volume1/main /mnt/nas nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0' >> /etc/fstab"

git config --global user.name "Tom O'Connell"
# could do email too just don't want to have it scrapable from github...

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

echo "To finish setting up OpenVPN, login to pfsense gateway from a computer "
echo "already on the VPN and make a new user named as this computer (check the "
echo "box to create a certificate while creating a user)."
echo ""
echo "Then export inline configurtion for that user and copy the .ovpn file to "
echo "/etc/openvpn, and rename it to hongvpn.conf"
echo ""
echo "In the same (/etc/openvpn) directory, make a file called "
echo "hong_vpn_auth_user_and_pass.txt, with the username on the first line, "
echo "and the pfsense password on the second line."
echo ""
echo "Run:"
echo "sudo systemctl enable openvpn@hongvpn.service"
echo "...to enable on boot"

echo ""
echo "AFTER you have done this, uncomment the nfs line in /etc/fstab to mount "
echo "the NAS at boot."

echo ""
echo "You may need to change settings in YAML files under ~/experiments"

echo "alias roslaunch='ROS_HOME=\`pwd\` roslaunch'" >> ~/.bash_aliases
echo "alias transfer_data='rsync -avPuz $HOME/experiments/ lab@cthulhu:/mnt/tb/original'" >> ~/.bash_aliases

