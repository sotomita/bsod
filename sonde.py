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
        raw_data_dir: Path,
        **kwargs,
    ) -> None:

        self.sonde_no = sonde_no
        self.launch_time = launch_time
        self.raw_data_dir = raw_data_dir
        self.raw_data_fpath = self.__get_raw_data_fpath()

    def __get_raw_data_fpath(self) -> Path:

        fpaths = list(self.raw_data_dir.glob(f"*S{self.sonde_no}.CSV"))

        if len(fpaths) == 0:
            raise FileNotFoundError(
                f"No raw data file found for sonde number {self.sonde_no} in {self.raw_data_dir}"
            )
        elif len(fpaths) > 1:
            warnings.warn(
                f"Multiple raw data files found for sonde number {self.sonde_no}. Using the first one.",
                UserWarning,
            )
        return fpaths[0]

    def raw_data(self) -> pd.DataFrame:

        if not self.raw_data_fpath.is_file():
            raise FileNotFoundError(
                f"Raw data file is not found: {self.raw_data_fpath}"
            )
        return pd.read_csv(self.raw_data_fpath, skiprows=6)

    def qc_data(self, qc_data_fpath: Path, recalc: bool = False) -> pd.DataFrame:
        self.qc_data_fpath = qc_data_fpath

        if not qc_data_fpath.exists():
            if not qc_data_fpath.parent.exists():
                warnings.warn(
                    f"The directory {qc_data_fpath.parent} does not exist and will be created.",
                    UserWarning,
                )
                qc_data_fpath.parent.mkdir(parents=True)

            # conduct QC processing
            raw_df = self.raw_data()
            qc_df = qc.get_qc_df(raw_df, self.sonde_no, self.launch_time)
            qc_df.to_csv(qc_data_fpath)
        else:
            if recalc:
                # conduct QC processing
                raw_df = self.raw_data()
                qc_df = qc.get_qc_df(raw_df, self.sonde_no, self.launch_time)
                qc_df.to_csv(qc_data_fpath)
            else:
                qc_df = pd.read_csv(qc_data_fpath)

        if qc_data_fpath is None or not qc_data_fpath.is_file():
            raise FileNotFoundError(f"QC data file is not found: {qc_data_fpath}")
        else:
            return pd.read_csv(qc_data_fpath)

    def __str__(self) -> str:

        return f"""
            Sonde {self.sonde_no}
            launch time {self.launch_time}
            raw data: {self.raw_data_fpath}
            qc data: {self.qc_data_fpath if hasattr(self, "qc_data_fpath") else ""}
        """
