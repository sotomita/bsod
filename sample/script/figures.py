#!/usr/bin/python3
# encoding utf-8 -*-

import os
import sys
import pandas as pd

sys.path.append("../../")

import bsod
from bsod.plots import plot_emagram, plot_trajectory_2d

fpath = "../data/field_book.csv"
qc_data_dir = "../data/qc_data"
fig_dir = "../fig"

os.makedirs(fig_dir, exist_ok=True)

fbook = bsod.get_fieldbook(fpath)


for i in range(len(fbook)):
    st_name = fbook["st_name"].iloc[i]
    launch_time = fbook["JSTtime"].iloc[i]
    sonde_no = fbook["sonde_no"].iloc[i]
    print("************************")
    print(st_name, launch_time, sonde_no)

    qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
    df = pd.read_csv(qcdata_fpath, index_col=0)

    # plot temperature emagram
    os.makedirs(f"{fig_dir}/emagram", exist_ok=True)
    plot_emagram(st_name, launch_time, df, f"{fig_dir}/emagram/{st_name}.png")
    """plot_trajectory_2d(
        {st_name: df},
        [135.5, 139.5, 33.5, 35.5],
        f"{fig_dir}/trajectory2d/{st_name}.png",
    )"""

    break
