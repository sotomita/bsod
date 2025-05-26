#!/usr/bin/python3
# -*- encoding utf-8 -*-

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

    sonde = bsod.Sonde(sonde_no, launch_time, st_name, raw_data_dir)
    print(sonde.raw_df.head())

    break
