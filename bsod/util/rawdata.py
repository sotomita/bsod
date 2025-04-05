#!/usr/bin/python3
# -*- encoding utf-8 -*-

from datetime import datetime
import pandas as pd


def get_raw_df(
    launch_time: datetime, sonde_no: str, parent_dir: str = "./", skiprows: int = 6
) -> pd.DataFrame:
    """Return raw data
    Parameters
    ----------
    launch_time :   datetime
        launch time(JST)
    sonde_no    :   str
        product number of radiosonde
    parent_dir    :   str
        file path of parent directory of raw data files
    Returns
    pd.DataFrame
        DataFrame with appropriate type conversion.
    ----------
    """

    fpath = f"{parent_dir}/F{launch_time.strftime('%Y%m%d%H')}S{sonde_no}.CSV"
    df = pd.read_csv(fpath, skiprows=skiprows)

    return df
