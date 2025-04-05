#!/usr/bin/python3
# -*- encoding utf-8 -*-

from datetime import datetime, timedelta
import pandas as pd


def numeric_condition_idx(df: pd.DataFrame, field: str, conditons: list):
    """return the indice that satisfy the condition
    Parameters
    ----------
    Returns
    ----------
    idx_all
        indice that satisfy the condition(s)
    """
    for i in range(len(conditons)):
        idx = pd.to_numeric(df[field], errors="coerce") == conditons[i]
        idx_all = idx_all | idx if i != 0 else idx

    return idx_all


def get_qcdata(
    raw_df: pd.DataFrame, launch_time: datetime, sonde_no: str
) -> pd.DataFrame:
    """get post QC data.
    Parameters
    ----------
    Returns
    ----------
    """

    df = raw_df.copy()

    # --- rename column name.

    df.columns = [c.replace(" ", "") for c in df.columns]

    # --- remove error records

    # observation status(ST)
    st = numeric_condition_idx(df, "ST", [7])
    # reciever error status(RE)
    re = numeric_condition_idx(df, "RE", [0, 4])
    # sonde No.(sondeN)
    sonden = df["SondeN"].astype(str) == sonde_no
    # GPS Flag(GF)
    gf = numeric_condition_idx(df, "GF", [4, 3, 2, 1])
    # meteorological variable status(VE,V)
    ve = numeric_condition_idx(df, "V", [0])
    # frequency error status(FE)
    fe = numeric_condition_idx(df, "FE", [0])
    # number of the GPS satellite(N)
    n = pd.to_numeric(df["N"], errors="coerce") >= 4

    condition = st & re & sonden & gf & ve & fe & n

    df = df[condition]
    remove_columns = ["ST", "RE", "SondeN", "AGC", "GF", "V", "FE", "N"]
    for col in remove_columns:
        del df[col]
    df = df.reset_index(drop=True)

    # --- time field
    df = df.rename(columns={"Time(LTUTC+09.0)": "Time"})
    time0 = datetime.strptime(df["Time"].iloc[0], "%H:%M:%S")
    time0 = datetime(
        launch_time.year,
        launch_time.month,
        launch_time.day,
        time0.hour,
        time0.minute,
        time0.second,
    )
    df.loc[0, "Time"] = time0
    for i in range(1, len(df)):
        time = datetime.strptime(df["Time"].iloc[i], "%H:%M:%S")
        time = datetime(
            time0.year, time0.month, time0.day, time.hour, time.minute, time.second
        )
        time = time + timedelta(days=1) if time < time0 else time
        df.loc[i, "Time"] = time
        time0 = time

    # --- cast some fields
    cast_fields = [
        "rcvFREQ",
        "WD",
        "WS",
        "Height",
        "Xdistanc",
        "Ydistanc",
        "GeodetLat",
        "GeodetLon",
        "Press0",
        "Temp0",
        "Humi0",
    ]
    for field in cast_fields:
        df[field] = pd.to_numeric(df[field], errors="coerce")

    return df
