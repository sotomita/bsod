#!/usr/bin/python3
# encoding utf-8 -*-

import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tqdm import tqdm

sys.path.append("../../")

import bsod
from bsod.plots import plot_emagram, plot_trajectory_2d, plot_trajectory_3d

fpath = "../data/field_book.csv"
qc_data_dir = "../data/qc_data"
var = sys.argv[1]
start_time = sys.argv[2]
start_time = datetime.strptime(start_time, "%Y-%m-%d_%H:%M:%S")
end_time = sys.argv[3]
end_time = datetime.strptime(end_time, "%Y-%m-%d_%H:%M:%S")
frame_delta_min = int(sys.argv[4])
frame_delta_time = timedelta(minutes=frame_delta_min)

plot_delta_min = int(sys.argv[5])
plot_delta_time = timedelta(minutes=plot_delta_min)
fig_dir = sys.argv[6]

# time list
time_list = []
time = start_time
while time <= end_time:
    time_list.append(time)
    time += frame_delta_time

plot_valid_time = start_time

fbook = bsod.get_fieldbook(fpath)


print(f"trajectory: {var}")
for plot_valid_time in tqdm(time_list):
    df_dict = {}
    for i in range(len(fbook)):
        st_name = fbook["st_name"].iloc[i]
        launch_time = fbook["JSTtime"].iloc[i]
        sonde_no = fbook["sonde_no"].iloc[i]
        qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
        df = pd.read_csv(qcdata_fpath, index_col=0)
        df["Time"] = pd.to_datetime(df["Time"])
        mask = (plot_valid_time - plot_delta_time <= df["Time"]) & (
            df["Time"] <= plot_valid_time
        )
        if len(df) > 0:
            df_dict[st_name] = df[mask]

    plot_trajectory_3d(
        df_dict,
        var_name=var,
        region=[136, 138, 34.0, 35.5, -4000, 15000],
        fig_path=f"{fig_dir}/{var}3d_{plot_valid_time.strftime('%Y-%m-%d_%H%M%S')}.png",
        azimuth=220,  # 180 : north up
        elevation=25,
        title=plot_valid_time.strftime("%Y-%m-%d %H:%M:%S"),
    )
