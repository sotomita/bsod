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

fpath = "../data/field_book.csv"
qc_data_dir = "../data/qc_data"
fig_dir = "../fig"

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
    print(f"trajectory 2D: {var}")
    os.makedirs(f"{fig_dir}/trajectory2d", exist_ok=True)
    plot_trajectory_2d(
        df_dict,
        var_name=var,
        plot_area=[135.5, 138.5, 34.0, 35.5],
        fig_path=f"{fig_dir}/trajectory2d/{var}.png",
        lon_ticks=np.arange(135.5, 138.6, 0.5),
        lat_ticks=np.arange(34.0, 35.6, 0.5),
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
    print(f"trajectory 3D: {var}")
    os.makedirs(f"{fig_dir}/trajectory3d", exist_ok=True)
    plot_trajectory_3d(
        df_dict,
        var_name=var,
        region=[136, 138, 34.0, 35.5, -4000, 15000],
        fig_path=f"{fig_dir}/trajectory3d/{var}3d.png",
        azimuth=220,  # 180 : north up
        elevation=25,
    )
