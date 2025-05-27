#! /usr/bin/env/python3
# -*- encoding utf-8 -*-

from subprocess import run
import os
import shutil

import namelist

# plot 3D trajectory animation

var_name = namelist.var_name
start_time = namelist.start_time
end_time = namelist.end_time
frame_delta_min = namelist.frame_delta_min
plot_delta_min = namelist.plot_delta_min
fig_dir = f"{namelist.fig_dir}/trajectory3d_animation/{var_name}"

if os.path.isdir(f"{fig_dir}/frame"):
    shutil.rmtree(f"{fig_dir}/frame")
os.makedirs(f"{fig_dir}/frame", exist_ok=True)


# plot frames
print("plot frames")
run(
    [
        "python3",
        "__frame_3d_trajectory.py",
        f"{var_name}",
        f"{start_time}",
        f"{end_time}",
        f"{frame_delta_min}",
        f"{plot_delta_min}",
        f"{fig_dir}/frame",
    ]
)

# gif
print("make GIF")
run(
    [
        "magick",
        "-delay",
        "30",
        "-loop",
        "0",
        f"{fig_dir}/frame/*png",
        f"{fig_dir}/{var_name}.gif",
    ]
)
