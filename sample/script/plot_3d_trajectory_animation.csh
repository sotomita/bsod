#!/usr/bin/csh

# plot 3D trajectory animation

set var_name = "rh"
set start_time = "2024-06-18_06:00:00"
set end_time = "2024-06-18_16:00:00"
set frame_delta_min = "3"
set plot_delta_min = "30"
set fig_dir = "../fig/trajectory3d_animation/${var_name}"

mkdir -p "${fig_dir}/frame"

# plot frames
echo "plot frames" 
python3 __frame_3d_trajectory.py \
    $var_name  $start_time $end_time $frame_delta_min $plot_delta_min \
    "${fig_dir}/frame" 

# gif
echo "make GIF"
convert -delay 30 -loop 0 "${fig_dir}/frame/*png" "${fig_dir}/${var_name}.gif"

echo "finish"