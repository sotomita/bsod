#!/usr/bin/python3
# -*- encoding utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def trajectory_2d(df, plot_area: list, fig_path: str) -> None:

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(1, 1, 1)
