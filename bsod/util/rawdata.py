#!/usr/bin/python3
# -*- encoding utf-8 -*-

from glob import glob
from datetime import datetime
import pandas as pd
import warnings
from warnings import WarningMessage


class SearchRawfileWarning(WarningMessage):
    pass


def get_raw_df(
    sonde_no: str,
    parent_dir: str = "./",
) -> pd.DataFrame:
    """Return raw data

    Parameters
    ----------
    sonde_no    :   str
        product number of radiosonde
    parent_dir    :   str
        file path of parent directory of raw data files

    Returns
    ----------
    pd.DataFrame
        DataFrame with appropriate type conversion.
    """

    fpaths = glob(f"{parent_dir}/*S{sonde_no}.CSV")
    if len(fpaths) == 0:
        warnings.warn("No rawdata file is found", SearchRawfileWarning)
        df = None

    if len(fpaths) >= 1:
        if len(fpaths) > 1:
            warnings.warn(
                "More than 1 file was found. The first one is read.",
                SearchRawfileWarning,
            )
        fpath = fpaths[0]
        df = pd.read_csv(fpath, skiprows=6)

    return df
