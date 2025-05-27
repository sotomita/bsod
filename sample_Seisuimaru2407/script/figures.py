#!/usr/bin/python3
# encoding utf-8 -*-

import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

sys.path.append("../../")

import bsod
from bsod.plots import plot_emagram, plot_trajectory_2d, plot_trajectory_3d
import namelist

fpath = namelist.fbook_path
qc_data_dir = namelist.qc_data_dir
fig_dir = namelist.fig_dir

os.makedirs(fig_dir, exist_ok=True)

fbook = bsod.get_fieldbook(fpath)


# plot emagram

print("*************************************")
print("emagram")
print("St. name\tJST time\tsonde No.")
for i in range(len(fbook)):
    st_name = fbook["st_name"].iloc[i]
    launch_time = fbook["JSTtime"].iloc[i]
    sonde_no = fbook["sonde_no"].iloc[i]
    print(f"{st_name}\t{launch_time}\t{sonde_no}")

    qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
    df = pd.read_csv(qcdata_fpath, index_col=0)

    # plot temperature emagram
    os.makedirs(f"{fig_dir}/emagram", exist_ok=True)
    plot_emagram(st_name, launch_time, df, f"{fig_dir}/emagram/{st_name}.png")

# plot 2d trajectory
df_dict = {}
for i in range(len(fbook)):
    st_name = fbook["st_name"].iloc[i]
    launch_time = fbook["JSTtime"].iloc[i]
    sonde_no = fbook["sonde_no"].iloc[i]
    qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
    df = pd.read_csv(qcdata_fpath, index_col=0)
    df_dict[st_name] = df

vars = ["height", "temp", "rh"]
print("*************************************")
for var in vars:
    print(f"trajectory: {var}")
    os.makedirs(f"{fig_dir}/trajectory2d", exist_ok=True)
    plot_trajectory_2d(
        df_dict,
        var_name=var,
        plot_area=namelist.plot_area[:4],
        fig_path=f"{fig_dir}/trajectory2d/{var}.png",
        lon_ticks=namelist.lon_ticks,
        lat_ticks=namelist.lat_ticks,
    )

# plot 3D trajectory
df_dict = {}
for i in range(len(fbook)):
    st_name = fbook["st_name"].iloc[i]
    launch_time = fbook["JSTtime"].iloc[i]
    sonde_no = fbook["sonde_no"].iloc[i]
    qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
    df = pd.read_csv(qcdata_fpath, index_col=0)
    df_dict[st_name] = df

vars = ["height", "temp", "rh"]
print("*************************************")
for var in vars:
    print(f"trajectory: {var}")
    os.makedirs(f"{fig_dir}/trajectory3d", exist_ok=True)
    plot_trajectory_3d(
        df_dict,
        var_name=var,
        region=namelist.plot_area,
        fig_path=f"{fig_dir}/trajectory3d/{var}3d.png",
        azimuth=namelist.azimuth,  # 180 : north up
        elevation=namelist.elevation,
    )
