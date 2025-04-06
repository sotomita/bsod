#!/usr/bin/python3
# -*- encoding utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def plot_trajectory_2d(df_dict: dict, plot_area: list, fig_path: str) -> None:

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
            plot_area[2] - 1e-2,
            plot_area[3] + 1e-2,
        ]
    )

    ax.set_xlabel("Londitude", fontsize=8)
    ax.set_ylabel("Latitude", fontsize=8)

    # grid lines
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(), color="gray", linestyle="--", draw_labels=True
    )
    gl.xlocator = mticker.FixedLocator(np.arange(100, 160, 0.5))
    gl.ylocator = mticker.FixedLocator(np.arange(20, 60, 0.5))
    gl.top_labels = False
    gl.right_labels = False

    # Coast lines
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, linestyle="-")
    ax.coastlines(color="k", linestyle="-")

    plt.savefig(fig_path, dpi=512)
