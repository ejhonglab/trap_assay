
### One-line install
```
curl -s https://raw.githubusercontent.com/ejhonglab/trap_assay/master/install.sh | bash
```
Just paste this in to a terminal, hit enter, and type in your password as needed.

### Dependencies

[tom-f-oconnell/usb_cam](https://github.com/tom-f-oconnell/usb_cam)
Definitely works with my fork, but may also work with upstream `usb_cam`.

[tom-f-oconnell/multi_tracker](https://github.com/tom-f-oconnell/multi_tracker)

[tom-f-oconnell/metatools](https://github.com/tom-f-oconnell/metatools)


Install these dependencies as you would install any ROS package from source, i.e.

- Make a catkin workspace
- Clone each repository to `<workspace>/src`
- `cd <workspace> && catkin_make`
- `source <workspace>/devel/setup.bash`
	- You can put this line in your `~/.bashrc` file, towards the bottom. If you do, make sure to put it AFTER the other line that sources some `setup.bash` file ROS uses.

### To run the experiment

- `cd` to a directory with configuration files for the tracking.
- Run ```ROS_HOME=`pwd` roslaunch trap_assay trap.launch```
  (although if the output of `alias roslaunch` starts with 
  ````ROS_HOME=`pwd` roslaunch```, then you can just run 
  ```roslaunch trap_assay trap.launch```)

#### Parameters to the launch file

- `video_only`: (default=`True`) The tracking only saves the background subtracted video, plus background frames, and some metadata. Nodes to do extra image processing and data association necessary to generate trajectories are not started.

