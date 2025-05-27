#! /usr/bin/env/python3
# -*- encoding utf-8 -*-

from subprocess import run
import os
import shutil

# plot 3D trajectory animation

var_name = "rh"
start_time = "2024-06-18_06:00:00"
end_time = "2024-06-18_16:00:00"
frame_delta_min = "120"
plot_delta_min = "60"
fig_dir = f"../fig/trajectory3d_animation/{var_name}"

if os.path.isdir(f"{fig_dir}/frame"):
    shutil.rmtree(f"{fig_dir}/frame")
os.makedirs(f"{fig_dir}/frame", exist_ok=True)


# plot frames
print("plot frames")
run(
    [
        "python",
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
        "convert",
        "-delay",
        "30",
        "-loop",
        "0",
        f"{fig_dir}/frame/*png",
        f"{fig_dir}/{var_name}.gif",
    ]
)
