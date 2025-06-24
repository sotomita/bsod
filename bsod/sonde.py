#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pandas as pd

from . import qc
from . import anl


class Sonde:
    def __init__(
        self,
        sonde_no: str,
        launch_timeUTC: datetime,
        st_name: str,
        raw_data_dir_list: list,
        qc_data_dir: str,
        anl_data_dir: str,
        conduct_qc: bool,
        **kwargs,
    ) -> None:

        self.sonde_no = sonde_no
        self.st_name = st_name
        self.raw_data_dir_list = raw_data_dir_list
        self.qc_data_dir = qc_data_dir
        self.anl_data_dir = anl_data_dir

        # time zone
        self.launch_timeUTC = launch_timeUTC

        # read df
        raw_df = qc.get_raw_df(self.sonde_no, self.raw_data_dir_list)

        # conduct QC
        if conduct_qc:
            qc_df = qc.get_qc_df(raw_df, self.sonde_no, self.launch_timeUTC)

            # save QC DataFrame
            qc_fpath = kwargs.get(
                "qc_fpath", f"{self.qc_data_dir}/{self.st_name}.csv"
            )
            qc_df.to_csv(qc_fpath)

    def get_raw_df(self) -> pd.DataFrame:
        """get raw DataFrame(Wrapper of qc.get_raw_df)

        Returns
        -------
        pd.DataFrame
            raw data DataFrame
        """

        return qc.get_raw_df(self.sonde_no, self.raw_data_dir_list)

    def get_qc_df(self) -> pd.DataFrame:
        """return post QC DataFrame

        Returns
        -------
        pd.DataFrame
            post QC DataFrame.
        """
        qc_df = pd.read_csv(
            f"{self.qc_data_dir}/{self.st_name}.csv",
            index_col=0,
            parse_dates=["TimeUTC"],
        )
        return qc_df

    def get_anl_df(
        self,
        rm_descending: bool = True,
        min_prs: float = 0,
        max_prs: float = 1100,
    ) -> pd.DataFrame:

        anl_df = anl.get_anl_df(self.get_qc_df(), rm_descending)

        anl_df = anl_df[anl_df["Pressure"] > min_prs]
        anl_df = anl_df[anl_df["Pressure"] < max_prs]
        anl_df = anl_df.reset_index(drop=True)

        return anl_df
