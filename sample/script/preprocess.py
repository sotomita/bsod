#!/usr/bin/python3
# -*- encoding utf-9 -*-

import os
import sys

sys.path.append("../../")
import bsod
import bsod.util as butil


fbook_path = "../data/field_book.csv"
raw_data_dir = "../data/raw_data"
qc_data_dir = "../data/qc_data"

os.makedirs(qc_data_dir, exist_ok=True)

fbook = bsod.get_fieldbook(fbook_path)


for i in range(len(fbook)):
    st_name = fbook["st_name"].iloc[i]
    launch_time = fbook["JSTtime"].iloc[i]
    sonde_no = fbook["sonde_no"].iloc[i]
    print("************************")
    print(st_name, launch_time, sonde_no)

    # get raw data
    df = butil.get_raw_df(launch_time, sonde_no, parent_dir=raw_data_dir)
    print(f"raw data\t: {len(df)} records")

    # get qc data
    df = butil.get_qcdata(df, launch_time, sonde_no)
    print(f"post qc data\t: {len(df)} records")

    qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
    df.to_csv(qcdata_fpath)
