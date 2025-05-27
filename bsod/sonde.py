#!/usr/bin/env/python3
# -*- encoding utf-8 -*-

from datetime import datetime
import pandas as pd

from .util import get_raw_df, get_qc_df


class Sonde:
    def __init__(
        self,
        sonde_no: int,
        launch_timeUTC: datetime,
        st_name: str = "",
        raw_data_dir: str = "./",
        qc_data_fpath=None,
    ) -> None:
        self.sonde_no = sonde_no
        self.st_name = st_name
        self.raw_data_dir = raw_data_dir

        # time zone
        self.launch_timeUTC = launch_timeUTC

        if qc_data_fpath is None:
            self.raw_df = get_raw_df(self.sonde_no, self.raw_data_dir)
            # QC
            self.qc_df = get_qc_df(
                self.raw_df, self.sonde_no, self.launch_timeUTC
            )
        else:
            self.qc_data_fpath = qc_data_fpath
            self.qc_df = pd.read_csv(qc_data_fpath)

    def save_qc_df(self, fpath):
        # self.qc_df.to_csv(fpath, index=False)
        self.qc_df.to_csv(fpath)
