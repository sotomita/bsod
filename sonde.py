#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path
import warnings
import pandas as pd

import qc


class Sonde:
    def __init__(
        self,
        sonde_no: str,
        launch_time: datetime,
        raw_data_fpath: Path,
        qc_data_fpath: Path | None = None,
        **kwargs,
    ) -> None:
        self.sonde_no = sonde_no
        self.launch_time = launch_time
        self.raw_data_fpath = raw_data_fpath
        self.qc_data_fpath = qc_data_fpath

    def __str__(self) -> str:
        return f"""
            Sonde {self.sonde_no}
            launch time {self.launch_time}
            raw data: {self.raw_data_fpath}
        """

    def raw_data(self) -> pd.DataFrame:
        if not self.raw_data_fpath.is_file():
            raise FileNotFoundError(
                f"Raw data file is not found: {self.raw_data_fpath}"
            )
        return pd.read_csv(self.raw_data_fpath, skiprows=6)

    def qc(self, fpath: Path) -> None:
        if fpath.exists():
            warnings.warn(
                f"The file {fpath} already exist and will be overwritten.", UserWarning
            )
        if not fpath.parent.exists():
            warnings.warn(
                f"The directory {fpath.parent} does not exist and will be created.",
                UserWarning,
            )
            fpath.parent.mkdir(parents=True)

        raw_df = self.raw_data()
        qc_df = qc.get_qc_df(raw_df, self.sonde_no, self.launch_time)
        qc_df.to_csv(fpath)
        self.qc_data_fpath = fpath

    def qc_data(self) -> pd.DataFrame:
        if self.qc_data_fpath is None or not self.qc_data_fpath.is_file():
            raise FileNotFoundError(f"QC data file is not found: {self.qc_data_fpath}")
        else:
            return pd.read_csv(self.qc_data_fpath)
