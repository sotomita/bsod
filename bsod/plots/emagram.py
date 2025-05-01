#!/usr/bin/python3
# -*- encoding utf-8 -*-

from datetime import datetime
import numpy as np
import pint
import pandas as pd
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.units import units


def neary_idx(array: np.ndarray, target: np.ndarray) -> list:
    near_idx = []
    for i in range(target.shape[0]):
        if array.nanmin() < target and target < array.nanmax():
            neari = np.abs(array - target).argmin()
            near_idx.append(neari)
    return near_idx


def temp_emagram(
    temp: pint.Quantity,
    dewpoint: pint.Quantity,
    wd: pint.Quantity,
    ws: pint.Quantity,
    prs: pint.Quantity,
    st_name: str = "",
    launch_time="",
    fig_path: str = "./",
) -> None:
    """plot temperature emagram

    Parameters
    ----------
    temp    :   pint.Quantity
        temperature
    dewpoint    :   pint.Quantity
        dewpoint
    prs :   pint.Quantity
        pressure
    wd  :   pint.Quantity
        wind direction
    ws  :   pint.Quantity
        wind speed
    st_name :   str, default=""
        station name
    launch_time :   datetime or str, default=""
        launch time
    fig_path    :   str, default="./"
        figure path

    Returns
    ----------
    None
    """

    # --- parameters ---
    # temperature
    tmin = -90
    tmax = 40
    tticks = np.arange(tmin, tmax + 1e-4, 10)
    tticks_minor = np.arange(tmin, tmax + 1e-4, 5)
    # pressure
    pmin = 100
    pmax = 1050
    pticks = np.arange(pmin, pmax + 1e-4, 100)
    # wind
    wind_target_p = np.arange(100, 1200, 25)

    # ---------------

    fig = plt.figure(figsize=(9, 12))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect(200)

    # title
    ax.set_title(f"{st_name}  {launch_time.strftime('%Y-%m-%d %H:%M')}", fontsize=15)

    # x axis(degC)
    ax.set_xlabel("[degC]")
    ax.set_xlim(tmin, tmax)
    ax.set_xticks(tticks)
    ax.set_xticks(tticks_minor, minor=True)

    # y axis (pressure)
    ax.set_ylabel("Pressure [hPa]")
    ax.set_ylim(pmin, pmax)
    ax.set_yscale("log")
    ax.invert_yaxis()
    ax.set_yticks(pticks)
    ax.set_yticklabels(pticks)
    ax.set_yticklabels([f"{int(p):d}" for p in pticks.tolist()])

    # grid line
    ax.grid(True, which="both", linewidth=0.5, color="gray")

    #

    # temperature - pressure
    ax.plot(temp, prs, c="r")

    # dewpoint - pressure
    ax.plot(dewpoint, prs, c="b")

    # dry-adiabatic line
    t0s = np.arange(240, 381, 10) * units("K")
    plev = np.arange(50, 1101) * units.hPa
    for i in range(t0s.shape[0]):
        t0 = t0s[i]
        dry_l = mpcalc.dry_lapse(plev, t0, 1000 * units.hPa).to("degC")
        ax.plot(dry_l, plev, c="k", linewidth="0.7")
        label_i = np.abs(dry_l - -88 * units("degC")).argmin()
        if plev[label_i] > 100.0 * units.hPa:
            ax.text(
                dry_l[label_i], plev[label_i], f"{int(t0.m)}", fontsize=7, color="k"
            )
        else:
            label_i = np.abs(plev - 102 * units.hPa).argmin()
            ax.text(
                dry_l[label_i], plev[label_i], f"{int(t0.m)}", fontsize=7, color="k"
            )

    # moist adiabatic line
    t0s = np.arange(240, 381, 10) * units("K")
    plev = np.arange(50, 1101) * units.hPa
    for i in range(t0s.shape[0]):
        t0 = t0s[i]
        dry_l = mpcalc.moist_lapse(plev, t0, 1000 * units.hPa).to("degC")
        ax.plot(dry_l, plev, c="k", linewidth="0.7")

    # wind array
    wind_i = neary_idx(prs, wind_target_p)
    wind_prs = prs[wind_i]
    wind_wd = prs[wind_i]
    wind_ws = prs[wind_i]

    plt.savefig(fig_path, dpi=512)
    plt.close()


def plot_emagram(
    st_name: str,
    launch_time: datetime,
    df: pd.DataFrame,
    fig_path: str,
    rm_descending: bool = True,
    mode: str = "temp",
) -> None:
    """wrapper for plot (temperature or potential temp.) emagram.

    Parameters
    ----------
    st_name :   str
        station name
    launch_time :   datetime
        launch time
    df  :   pd.DataFrame
        post-QC data
    fig_path    :   str
        figure path
    rm_descinding   :   bool, default=True
    mode    :   str
        "temp" for plot the temperature emagram

    Returns
    ----------
    None
    """
    df = df.copy()

    # remove descending record
    if rm_descending:
        max_i = df["Height"].idxmax()
        df = df.drop(index=range(max_i + 1, len(df)))

    # temperature emagram
    if mode == "temp":
        temp = df["Temp0"].values * units("degC")
        rh = df["Humi0"].values * 1e-2
        rh[rh <= 0] = np.nan
        wd = df["WD"].values * units("deg")
        ws = df["WS"].values * units("m/s")
        prs = df["Press0"].values * units("hPa")
        dewpoint = mpcalc.dewpoint_from_relative_humidity(temp, rh)
        temp_emagram(temp, dewpoint, wd, ws, prs, st_name, launch_time, fig_path)
