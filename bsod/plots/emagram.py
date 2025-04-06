#!/usr/bin/python3
# -*- encoding utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.units import units


def temp_emagram(temp, dewpoint, prs) -> None:
    """plot temperature emagram
    Parameters
    ----------
    Returns
    ----------
    """
    pass


def plot_emagram(df: pd.DataFrame, fig_path: str) -> None:
    """ """
    df = df.copy()
    max_i = df["Height"].idxmax()
    df = df.drop(index=range(max_i + 1, len(df)))

    temp = df["Temp0"].values * units("degC")
    rh = df["Humi0"].values * 1e-2
    rh[rh <= 0] = np.nan
    prs = df["Press0"].values * units("hPa")
    dewpoint = mpcalc.dewpoint_from_relative_humidity(temp, rh)

    tmin = -90
    tmax = 40
    tticks = np.arange(tmin, tmax + 1e-4, 10)
    tticks_minor = np.arange(tmin, tmax + 1e-4, 5)
    pmin = 100
    pmax = 1050
    pticks = np.arange(pmin, pmax + 1e-4, 100)

    fig = plt.figure(figsize=(9, 12))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect(200)

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

    plt.savefig(fig_path, dpi=512)
