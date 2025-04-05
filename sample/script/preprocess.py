#!/usr/bin/python3
# -*- encoding utf-9 -*-

import sys

sys.path.append("../../")
import bsod
import bsod.util as butil


fpath = "../data/field_book.csv"
fbook = bsod.get_fieldbook(fpath)


for i in range(len(fbook)):
    st_name = fbook["st_name"].iloc[i]
    launch_time = fbook["JSTtime"].iloc[i]
    sonde_no = fbook["sonde_no"].iloc[i]
    print("************************")
    print(st_name, launch_time, sonde_no)

    # get raw data
    df = butil.get_raw_df(launch_time, sonde_no, parent_dir="../data/raw_data")
    print(df.head())
    print(len(df))

    # get qc data
    df = butil.get_qcdata(df, launch_time, sonde_no)

    print(df.head())
    # print(df.dtypes)
    print(len(df))

    qcdata_fpath = f"../data/qc_data/{st_name}.csv"
    df.to_csv(qcdata_fpath)
