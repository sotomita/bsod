#!/usr/bin/python3
# -*- encoding utf-8 -*-

import pandas as pd


def get_fieldbook(fpath: str) -> pd.DataFrame:
    """read field book as DataFrame.

    Parameters
    ----------
    fpath   :   str
        file path of field book(.csv)

    Returns
    ----------
    pd.DataFrame
        DataFrame with appropriate type conversion.
    """

    df = pd.read_csv(
        fpath,
        dtype={
            "st_name": str,
            "JSTtime": str,
            "sonde_no": str,
        },
    )

    df["JSTtime"] = pd.to_datetime(df["JSTtime"].str.replace("_", " "))
    return df
