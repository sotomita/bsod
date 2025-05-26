#!/usr/bin/python3
# -*- encoding utf-8 -*-

from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def numeric_condition_idx(df: pd.DataFrame, field: str, conditons: list):
    """return indice that satisfy the condition

    Parameters
    ----------
    df  :   pd.DataFrame
    field   :   str
        field (column) that focused on.
    conditions  :   list

    Returns
    ----------
    idx_all
        indice that satisfy the condition(s)

    """
    idx_all = False
    for i in range(len(conditons)):
        idx = pd.to_numeric(df[field], errors="coerce") == conditons[i]
        idx_all = idx_all | idx if i != 0 else idx

    return idx_all


def get_qc_df(
    raw_df: pd.DataFrame,
    sonde_no: str,
    launch_time: datetime,
) -> pd.DataFrame:

    df = raw_df.copy()

    # --- rename column name.
    df.columns = [c.replace(" ", "") for c in df.columns]

    # --- remove error records.
    # observation status(ST)
    st = numeric_condition_idx(df, "ST", [7])
    # reciever error status(RE)
    re = numeric_condition_idx(df, "RE", [0, 4])
    # sonde No.(sondeN)
    sonden = df["SondeN"].astype(str) == sonde_no
    # GPS Flag(GF)
    gf = numeric_condition_idx(df, "GF", [4, 3, 2, 1])
    # number of the GPS satellite(N)
    n = pd.to_numeric(df["N"], errors="coerce") >= 4

    condition = st & re & sonden & gf & n
    df = df[condition]
    remove_columns = ["ST", "SondeN", "AGC", "GF", "N"]
    for col in remove_columns:
        del df[col]
    df = df.reset_index(drop=True)

    # VE
    ve = pd.to_numeric(df["V"], errors="coerce").values
    prs_e = np.zeros_like(ve)
    tmp_e = np.zeros_like(ve)
    hum_e = np.zeros_like(ve)
    for i in range(ve.shape[0]):
        b = format(ve[i], "03b")
        hum_e[i] = 1 if b[0] == 1 else 0
        tmp_e[i] = 1 if b[1] == 1 else 0
        prs_e[i] = 1 if b[2] == 1 else 0

    return df
