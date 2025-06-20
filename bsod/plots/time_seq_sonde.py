#!/usr/bin/env python3
# use to copy this to 'script' directory

import os, sys
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["font.size"]=14
import matplotlib.dates as mdates
sys.path.append("../../")
import bsod
from bsod.plots import plot_emagram, plot_trajectory_2d, plot_trajectory_3d
import namelist

fpath = namelist.fbook_path
qc_data_dir = namelist.qc_data_dir
fig_dir = namelist.fig_dir
fbook = bsod.get_fieldbook(fpath)

# available variables
#'TimeUTC', 'DCnt', 'RE', 'FCnt', 'rcvFREQ', 'WM', 'WD', 'WS', 'Height',
#'Xdistanc', 'Ydistanc', 'HDP', 'PDP', 'GeodetLat', 'GeodetLon', 'V',
#'FE', 'FRT', 'FTI', 'FVH', 'FVL', 'FSP1', 'FSP2', 'FSP3', 'FSP4', 'N',
#'Prs', 'Tmp', 'Hum'
# and available calculated variables
# 'Pot': potential temperature

var = 'Hum'

# top pressure of figure
top = 300

# range of pressure level
p = np.arange(1050,top,-1)

# range of times
times = pd.date_range("2024-06-18 07", "2024-06-18 18", freq="h")

######################### no need to edit below 

fdir = f'{fig_dir}/time_seq'
os.makedirs(fdir,exist_ok=True)
fig_path = f'{fdir}/{var}.png'
    

def draw_time_seq(x,p,ar,top):

    ax = plt.axes()
    #shade=ax.contourf(times,p,ar)#,np.arange(290,320,1))
    shade=ax.pcolormesh(times,p,ar)#,np.arange(290,320,1))
    plt.colorbar(shade)

    ax.set_ylim([1000,top])

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%H"))
    plt.xticks(rotation=45)

    ax.set_title(var)

    plt.tight_layout()
    plt.savefig(fig_path, dpi=512)

def calc_pot(t,p):
    k = 2/7
    return t * ((1000/p) ** k)

def check_time(launch_time):

    launch_time_pd = pd.to_datetime(launch_time) + pd.Timedelta(minutes=30)
    nearest_00_time = launch_time_pd.round("h")
    for i,t in enumerate(times):
        if t == nearest_00_time:
            return i
    print("no matched time, change range of times")
    exit()

def main():

    csvs = glob(f'{qc_data_dir}/*csv')

    N = len(times)
    x = np.arange(N)
    ar = np.full((len(p),N),np.nan)

    print("St. name\tJST time\tsonde No.")
    for j in range(len(fbook)):
        st_name = fbook["st_name"].iloc[j]
        launch_time = fbook["JSTtime"].iloc[j]
        sonde_no = fbook["sonde_no"].iloc[j]
        print(f"{st_name}\t{launch_time}\t{sonde_no}")

        qcdata_fpath = f"{qc_data_dir}/{st_name}.csv"
        df = pd.read_csv(qcdata_fpath, index_col=0)

        idx_t = check_time(launch_time)

        P = df['Prs']
        Z = df['Height'].values

        if var == 'Pot':
            A = df['Tmp'].values + 273.15
            A = calc_pot(A,P)
        else:
            A = df[var].values

        idx_p = [True if _p in P else False for _p in p]
        P_min = np.nanmin(P)
        P_max = np.nanmax(P)
        #print(P_max,P_min)
        idx_0 = 0
        idx_1 = len(p)
        inner = False
        for i,_p in enumerate(p):
            if _p == P_max:
                idx_0 = i
            if _p == P_min:
                inner = True
                idx_1 = i + 1
                break

        if not inner:
            A = A[:idx_1-idx_0]

        ar[idx_0:idx_1,idx_t] = A

    # unwanted columns
    #ar[:,5] = np.nan
    #ar[:,8] = np.nan

    draw_time_seq(x,p,ar,top)
    print("done.")

main()
