#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append("./")

if __name__ == "__main__":

    import os
    from datetime import timedelta

    from bsod.sonde import Sonde
    from bsod import get_fieldbook

    import namelist as nl

    print("preprocess.py")

    # directory setting
    os.makedirs(nl.qc_data_dir, exist_ok=True)
    os.makedirs(nl.anl_data_dir, exist_ok=True)

    # read field book
    fbook_df = get_fieldbook(nl.fbook_fpath)

    for i in range(len(fbook_df)):
        st_name = fbook_df["st_name"].iloc[i]
        launch_time = fbook_df["JSTtime"].iloc[i]
        launch_timeUTC = launch_time - timedelta(hours=9)
        sonde_no = fbook_df["sonde_no"].iloc[i]

        print("************************")
        print(st_name, launch_time, sonde_no)

        """if st_name != "St.4f":
            continue"""

        # Sonde class
        sonde = Sonde(
            sonde_no,
            launch_timeUTC,
            st_name,
            nl.raw_data_dir_list,
            nl.qc_data_dir,
            nl.anl_data_dir,
            conduct_qc=True,
        )
