#! /usr/bin/env python3

import numpy as np
import pandas as pd
import metpy.calc as mpcalc
from metpy.units import units
import matplotlib.pyplot as plt


def get_anl_df(qc_df: pd.DataFrame, min_z: float = 0) -> pd.DataFrame:

    # remove records observed above the maximum height
    max_z_idx = qc_df["Height"].idxmax()
    qc_df = qc_df.loc[:max_z_idx].reset_index(drop=True)

    # remove dessicated records
    qc_df["dz"] = qc_df["Height"].diff().fillna(0)
    qc_df = qc_df[qc_df["dz"] > 0]

    # remove records below the minimum height
    qc_df = qc_df[qc_df["Height"] >= min_z].reset_index(drop=True)

    # time
    time_utc = pd.to_datetime(qc_df["TimeUTC"])
    time_jst = time_utc + pd.Timedelta(hours=9)

    # location
    lon = qc_df["GeodetLon"].values * units("deg")
    lat = qc_df["GeodetLat"].values * units("deg")
    x = qc_df["Xdistanc"].values * units("m")
    y = qc_df["Ydistanc"].values * units("m")

    # temperature
    tmp = qc_df["Tmp"].values * units("degC")

    # elevation
    z = qc_df["Height"].values * units("m")
    prs = qc_df["Prs"].values * units("hPa")

    # Humidity
    rh = qc_df["Hum"].values * units("percent")
    dewpoint = mpcalc.dewpoint_from_relative_humidity(tmp, rh)
    mixr = mpcalc.mixing_ratio_from_relative_humidity(prs, tmp, rh)
    spc_hum = mpcalc.specific_humidity_from_mixing_ratio(mixr)

    # wind
    wd = qc_df["WD"].values * units("deg")
    ws = qc_df["WS"].values * units("m/s")
    u, v = mpcalc.wind_components(ws, wd)

    pt = mpcalc.potential_temperature(prs, tmp)
    ept = mpcalc.equivalent_potential_temperature(prs, tmp, dewpoint)

    anl_df = pd.DataFrame(
        {
            "TimeUTC": time_utc,
            "TimeJST": time_jst,
            "lon": lon.m,
            "lat": lat.m,
            "x": x.m,
            "y": y.m,
            "z": z.m,
            "prs": prs.m,
            "tmp": tmp.m,
            "rh": rh.m,
            "dewpoint": dewpoint.m,
            "mixr": mixr.m,
            "spc_hum": spc_hum.m,
            "wd": wd.m,
            "ws": ws.m,
            "u": u.m,
            "v": v.m,
            "pt": pt.m,
            "ept": ept.m,
        }
    )

    return anl_df
