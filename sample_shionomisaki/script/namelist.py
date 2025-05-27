#!/usr/bin/env/python3
# -*- encoding utf-8 -*-

import numpy as np

fbook_path = "../data/field_book.csv"
raw_data_dir = "../data/raw_data"
qc_data_dir = "../data/qc_data"
fig_dir = "../fig"

# 2D/3D trajectory
plot_area = [135.5, 137.1, 33.0, 34.0, -4000, 15000]

# 2D trajectory
lon_ticks = np.arange(135.5, 137.1, 0.25)
lat_ticks = np.arange(33.0, 34.1, 0.25)

# 3D trajectory
azimuth = 240  # 180 : north up
elevation = 25

# 3D trajectory animation
var_name = "rh"
start_time = "2025-05-08_09:00:00"
end_time = "2025-05-08_17:30:00"
frame_delta_min = "5"
plot_delta_min = "20"
