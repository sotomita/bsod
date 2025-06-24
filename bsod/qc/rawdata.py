#!/usr/bin/python3
# -*- encoding utf-8 -*-

from glob import glob
import pandas as pd
import warnings


def get_raw_df(
    sonde_no: str,
    parent_dir_list: list,
) -> pd.DataFrame:
    """Return raw data

    Parameters
    ----------
    sonde_no    :   str
        product number of radiosonde
    parent_dir_list    :   list
        file path list of parent directory of raw data files

    Returns
    ----------
    pd.DataFrame
        DataFrame with appropriate type conversion.
    """

    fpaths = []
    for parent_dir in parent_dir_list:
        fpaths += glob(f"{parent_dir}/*S{sonde_no}.CSV")

    if len(fpaths) == 0:
        raise FileNotFoundError(
            f"raw data file {sonde_no} is not Found in '{parent_dir}'"
        )

    if len(fpaths) >= 1:
        if len(fpaths) > 1:
            warnings.warn(
                "More than 1 file is found. The first one is read.",
                UserWarning,
            )
        fpath = fpaths[0]
        df = pd.read_csv(fpath, skiprows=6)

    return df
