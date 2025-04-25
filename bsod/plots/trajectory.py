#!/usr/bin/python3
# -*- encoding utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def plot_trajectory_2d(
    df_dict: dict, var_name: str, plot_area: list, fig_path: str, **kwargs
) -> None:
    """
    _summary_

    Parameters
    ----------
    df_dict : dict
        _description_
    plot_area : list
        _description_
    fig_path : str
        _description_
    """
    central_longitude = kwargs.get("central_longitude", 135)
    if "cmap" in kwargs:
        cmap = kwargs.get("cmap")
    else:
        if var_name == "height":
            cmap = "viridis"
        elif var_name == "temp":
            cmap = "turbo"
        elif var_name == "rh":
            cmap = "rainbow_r"
    if "cbar_ticks" in kwargs:
        cbar_ticks = kwargs.get("cbar_ticks")
    else:
        if var_name == "height":
            cbar_ticks = np.arange(0, 16001, 2000)
            vmin = 0
            vmax = 16000
        elif var_name == "temp":
            cbar_ticks = np.arange(-50, 41, 10)
            vmin = -50
            vmax = 41
        elif var_name == "rh":
            cbar_ticks = np.arange(0, 101, 10)
            vmin = 0
            vmax = 100

    colors = cm.Set1(np.arange(len(df_dict)))

    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(
        1,
        1,
        1,
        projection=ccrs.Mercator(
            central_longitude=(plot_area[1] - plot_area[0]) / 2.0,
            min_latitude=plot_area[2],
            max_latitude=plot_area[3],
        ),
    )

    ax.set_extent(
        [
            plot_area[0] - 1e-2,
            plot_area[1] + 1e-2,
            plot_area[2] - 5e-2,
            plot_area[3] + 1e-2,
        ]
    )

    # x axis
    ax.set_xlabel("Londitude", fontsize=8)

    # y axis
    ax.set_ylabel("Latitude", fontsize=8)

    # grid lines and ticks
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(), color="gray", linestyle="--", draw_labels=True
    )
    if "lon_ticks" in kwargs:
        lon_ticks = kwargs.get("lon_ticks")
    gl.xlocator = mticker.FixedLocator(lon_ticks)
    if "lat_ticks" in kwargs:
        lat_ticks = kwargs.get("lat_ticks")
    gl.ylocator = mticker.FixedLocator(lat_ticks)
    gl.top_labels = False
    gl.right_labels = False

    # Coast lines
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, linestyle="-")
    ax.coastlines(color="k", linestyle="-")

    st_name_list = list(df_dict.keys())
    df_list = list(df_dict.values())
    for i in range(len(st_name_list)):
        st_name = st_name_list[i]
        df = df_list[i]
        lon = df["GeodetLon"].values
        lat = df["GeodetLat"].values
        if var_name == "height":
            var = df["Height"].values
        elif var_name == "temp":
            var = df["Temp0"].values
        elif var_name == "rh":
            var = df["Humi0"].values

        sc = ax.scatter(
            lon,
            lat,
            c=var,
            transform=ccrs.PlateCarree(),
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            s=10,
            zorder=1,
        )

        ax.scatter(
            lon[0],
            lat[0],
            s=80,
            transform=ccrs.PlateCarree(),
            marker="*",
            color=colors[i],
            label=st_name,
            zorder=2,
        )
        ax.scatter(
            lon[-1],
            lat[-1],
            s=100,
            transform=ccrs.PlateCarree(),
            marker="x",
            color=colors[i],
            zorder=2,
        )

    cbar = plt.colorbar(sc, ax=ax, orientation="horizontal")
    cbar.set_ticks(cbar_ticks)
    if var_name == "Height":
        cbar_label = "Height [m]"
    elif var_name == "temp":
        cbar_label = "Temperature [degC]"
    elif var_name == "rh":
        cbar_label = "RH [%]"
    else:
        cbar_label = ""
    cbar.set_label(cbar_label)

    ax.legend()

    plt.tight_layout()
    plt.savefig(fig_path, dpi=512)
