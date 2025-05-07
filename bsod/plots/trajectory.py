#!/usr/bin/python3
# -*- encoding utf-8 -*-

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pygmt


def plot_trajectory_2d(
    df_dict: dict, var_name: str, plot_area: list, fig_path: str, **kwargs
) -> None:
    """
    plot 2d trajectories with a variable(e.g. temperature,RH).

    Parameters
    ----------
    df_dict : dict
        dictionary of the post-QC data.
        key: station name
        value: post-QC data(pd.DataFrame)
    var_name : str
        variable name
    plot_area : list
        [min_lon,max_lon,min_lat,max_lat]
    fig_path : str
        file path of the output figure.
    """

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


def plot_trajectory_3d(
    df_dict: dict,
    var_name: str,
    region: list,
    fig_path: str,
    **kwargs,
) -> None:

    if "azimuth" in kwargs.keys():
        azimuth = kwargs.get("azimuth")
    else:
        azimuth = 135
    if "elevation" in kwargs.keys():
        elev = kwargs.get("elevation")
    else:
        elev = 20

    if var_name == "height":
        cbar_label = "Height [m]"
        series = [0, 15000]
        cmap = "turbo"
    elif var_name == "temp":
        cbar_label = "Temperature [degC]"
        series = [-50, 40]
        cmap = "turbo"
    elif var_name == "rh":
        cbar_label = "RH [%]"
        series = [0, 100]
        cmap = "seis"
    else:
        cbar_label = ""
    if "cmap" in kwargs.keys():
        cmap = kwargs.get("cmap")
    if "title" in kwargs.keys():
        title = kwargs.get("title")
    else:
        title = ""

    grid = pygmt.datasets.load_earth_relief(
        resolution="01m",
        region=region,
    )
    fig = pygmt.Figure()

    fig.grdview(
        grid=grid,
        perspective=[azimuth, elev],
        region=region,
        frame=["xaf", "yaf", "zafg1000+lElevation (m)", f"+t{title}"],
        shading=True,
        surftype="s",
        cmap="geo",
        projection="X10c/6c",
        zscale=0.0002,
    )

    # fig.colorbar(frame=["af", "y+lElevation (m)"])

    pygmt.makecpt(cmap=cmap, series=series)

    st_name_list = list(df_dict.keys())
    df_list = list(df_dict.values())
    for i in range(len(st_name_list)):
        st_name = st_name_list[i]
        df = df_list[i]
        if len(df) == 0:
            continue

        lon = df["GeodetLon"].values
        lat = df["GeodetLat"].values
        z = df["Height"].values
        if var_name == "height":
            var = df["Height"].values
        elif var_name == "temp":
            var = df["Temp0"].values
        elif var_name == "rh":
            var = df["Humi0"].values

        fig.plot3d(
            x=lon,
            y=lat,
            z=z,
            style="u0.05c",
            fill=var,
            cmap=True,
            perspective=[azimuth, elev],
            zscale=0.0002,
        )

    with fig.shift_origin(xshift=0):
        fig.colorbar(frame=f"xaf+l {cbar_label}")

    fig.savefig(fig_path)
