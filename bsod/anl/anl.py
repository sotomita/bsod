#!/usr/bin/env python3

import numpy as np
import pandas as pd
import metpy.calc as mpcalc
from metpy.units import units

from . import index

# import index


def read_qc_df(st_name: str, qc_data_dir: str) -> pd.DataFrame:
    fpath = f"{qc_data_dir}/{st_name}.csv"
    df = pd.read_csv(fpath, index_col=0)

    return df


def get_anl_df(
    qc_df: pd.DataFrame, rm_descending: bool = True
) -> pd.DataFrame:

    # rm NaN
    qc_df = qc_df.dropna(subset="Prs").reset_index(drop=True)

    # rm decending
    if rm_descending:
        qc_df = index.rm_decending(qc_df)

    # Linear interpolation
    p_min = int(qc_df["Prs"].min()) + 1
    p_max = int(qc_df["Prs"].max())
    p_arange = np.arange(p_max, p_min, -1)
    qc_df = qc_df.set_index("Prs")
    qc_df = qc_df.reindex(p_arange).interpolate(method="linear")
    qc_df = qc_df.reset_index().rename(columns={"index": "Prs"})

    time = qc_df["TimeUTC"]
    """time = [
        datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
        for t in qc_df["TimeUTC"].values
    ]"""
    hgt = qc_df["Height"].values * units("m")
    prs = qc_df["Prs"].values * units("hPa")
    tmp = qc_df["Tmp"].values * units("degC")
    rh = qc_df["Hum"].values * units("percent")
    wd = qc_df["WD"].values * units("deg")
    ws = qc_df["WS"].values * units("m/s")
    lon = qc_df["GeodetLon"].values * units("deg")
    lat = qc_df["GeodetLat"].values * units("deg")

    # Mixing ratio
    mix_r = mpcalc.mixing_ratio_from_relative_humidity(prs, tmp, rh)
    # dewpoint
    # rh_pisitive_idx = rh <= 0.0
    dewpoint = mpcalc.dewpoint_from_relative_humidity(tmp, rh)
    # wind component
    u, v = mpcalc.wind_components(ws, wd)
    # Potential Temperature
    pt = mpcalc.potential_temperature(prs, tmp)
    # Equivalent potential Temperature
    ept = mpcalc.equivalent_potential_temperature(prs, tmp, dewpoint)
    # LCL
    lcl_p, lcl_t = mpcalc.lcl(prs, tmp, dewpoint)

    df = pd.DataFrame(
        {
            "Time": time,
            "Height": hgt.m,
            "Longitude": lon.m,
            "Latitude": lat.m,
            "WD": wd.m,
            "WS": ws.m,
            "U": u.m,
            "V": v.m,
            "Pressure": prs.m,
            "Temperature": tmp.m,
            "Potential_Temp": pt.m,
            "Eq_Potential_Temp": ept.m,
            "RH": rh.m,
            "Mixing_ratio": mix_r.m,
            "Dewpoint": dewpoint.m,
            "LCL_p": lcl_p,
            "LCL_t": lcl_t,
        }
    )

    return df


if __name__ == "__main__":
    print("anl.py")

    qc_data_dir = "/home/aoi/research/bsod/sample/data/qc_data"
    st_name = "St.4f"

    qc_df = pd.read_csv(f"{qc_data_dir}/{st_name}.csv", index_col=0)

    df = get_anl_df(qc_df)
    print(df.head())
