#!/usr/bin/env python3

import os
import sys
from datetime import timedelta

sys.path.append("../../")
import bsod
import bsod.util as butil
import namelist

fbook_path = namelist.fbook_path
raw_data_dir = namelist.raw_data_dir
qc_data_dir = namelist.qc_data_dir

os.makedirs(qc_data_dir, exist_ok=True)

fbook = bsod.get_fieldbook(fbook_path)

for i in range(len(fbook)):
    st_name = fbook["st_name"].iloc[i]
    launch_time = fbook["JSTtime"].iloc[i]
    launch_timeUTC = launch_time - timedelta(hours=9)
    sonde_no = fbook["sonde_no"].iloc[i]
    print("************************")
    print(st_name, launch_time, sonde_no)

    sonde = bsod.Sonde(sonde_no, launch_timeUTC, st_name, raw_data_dir)
    qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
    sonde.save_qc_df(qcdata_fpath)
