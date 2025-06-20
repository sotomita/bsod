#!/usr/bin/env python3

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
