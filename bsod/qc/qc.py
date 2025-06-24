#!/usr/bin/env/python3
# -*- encoding utf-8 -*-

from datetime import datetime, timedelta
import math
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
    launch_timeUTC: datetime,
) -> pd.DataFrame:
    """get post QC data.

    Parameters
    ----------
    raw_df : pd.DataFrame
        raw data
    sonde_no : str
        sonde No.
    launch_timeUTC : datetime
        launch time

    Returns
    -------
    pd.DataFrame
        post QC data
    """

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
    df = df.reset_index(drop=True)

    # ---- time control
    time_cname = df.columns[0]
    time_zone = time_cname.replace("Time(LTUTC", "").replace(")", "")
    time_zone = float(time_zone)
    launch_time = launch_timeUTC + timedelta(hours=time_zone)
    df = df.rename(columns={time_cname: "Time"})
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
            time0.year,
            time0.month,
            time0.day,
            time.hour,
            time.minute,
            time.second,
        )
        time = time + timedelta(days=1) if time < time0 else time
        df.loc[i, "Time"] = time
        time0 = time
    for i in range(len(df)):
        df.loc[i, "Time"] -= timedelta(hours=time_zone)
    df = df.rename(columns={"Time": "TimeUTC"})

    # --- error control
    prs = pd.to_numeric(df["Press0"], errors="coerce").values
    tmp = pd.to_numeric(df["Temp0"], errors="coerce").values
    hum = pd.to_numeric(df["Humi0"], errors="coerce").values

    # VE
    ve = pd.to_numeric(df["V"], errors="coerce").values
    for i in range(ve.shape[0]):
        b = format(ve[i], "03b")
        hum[i] = np.nan if b[0] == 1 else hum[i]
        tmp[i] = np.nan if b[1] == 1 else tmp[i]
        prs[i] = np.nan if b[2] == 1 else prs[i]

    # FE
    fe = pd.to_numeric(df["FE"], errors="coerce").values
    fcnts = pd.to_numeric(df["FCnt"], errors="coerce").values
    for i in range(fe.shape[0]):
        fcnt = fcnts[i]
        if math.isnan(fcnt):
            hum[i] = np.nan
            tmp[i] = np.nan
            prs[i] = np.nan
            continue
        fcnt = int(fcnt)
        hx = fe[i]
        if math.isnan(hx):
            hum[i] = np.nan
            tmp[i] = np.nan
            prs[i] = np.nan
        else:
            hx = f"{int(hx):04d}"
            if int(hx[0]) != 0:
                hum[i] = np.nan
                tmp[i] = np.nan
                prs[i] = np.nan
                continue
            hx1 = format(int(hx[1]), "03b")
            if int(hx1[0]) == 1 and fcnt % 2 == 0:
                tmp[i] = np.nan
            if int(hx1[1]) == 1 and fcnt % 2 == 0:
                hum[i] = np.nan
            if int(hx1[2]) == 1 and fcnt % 2 == 0:
                prs[i] = np.nan
            hx2 = format(int(hx[2]), "03b")
            if int(hx2[0]) == 1 and fcnt % 2 == 1:
                tmp[i] = np.nan
            if int(hx2[1]) == 1 and fcnt % 2 == 1:
                hum[i] = np.nan
            if int(hx2[2]) == 1 and fcnt % 2 == 1:
                prs[i] = np.nan

    df["Prs"] = prs
    df["Tmp"] = tmp
    df["Hum"] = hum

    remove_columns = [
        "ST",
        "SondeN",
        "AGC",
        "GF",
        "N1",
        "N2",
        "N3",
        "N4",
        "N5",
        "N6",
        "N7",
        "N8",
        "Press0",
        "Temp0",
        "Humi0",
    ]
    for col in remove_columns:
        del df[col]
    df = df.reset_index(drop=True)

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
        "Prs",
        "Tmp",
        "Hum",
    ]
    for field in cast_fields:
        df[field] = pd.to_numeric(df[field], errors="coerce")

    return df
