# BSoD
<p>
<img src="https://img.shields.io/github/license/sotomita/bsod">
<img src="https://img.shields.io/github/languages/code-size/sotomita/bsod">
<img src="https://img.shields.io/github/downloads/sotomita/bsod/total">
<img src="https://img.shields.io/badge/-Python-gray.svg?logo=Python">
</p>
BSoD(BalloonScope on Deck) is a package in Python for reading and visualizing radiosonde data.  
This module was developed for Seisui-maru 2407 cruise.

<p align="center">
<img src="./sample_fig/emagram.png" alt="emagram" width="200"/>
<img src="./sample_fig/trj_2d_rh.png" alt="RH 2D trajectory" width="200"/><br>
<img src="./sample_fig/trj_3d_animation_rh.gif" alt="RH 2D trajectory" width="400"/>
</p>

## Dependencies
Required packages (tested versions):
- Python (3.13.3)
- Numpy (2.2.5)
- Pandas (2.2.3)
- Matplotlib (3.10.1)
- Cartopy (0.24.0)
- MetPy (1.7.0)
- PyGMT (0.15.0)

To run ```plot_3d_trajectory_animation.csh```, the following are required
- tqdm (4.67.1)
- ImageMagick  (7.1.1-47)
  
(example: Anaconda env.)
```
conda install -c conda-forge numpy pandas matplotlib cartopy metpy pygmt tqdm imagemagick
```   
## Usage
See also ```sample_Seisuimaru2407/script```.  
### Data Quality Control
#### 1. Prepare field_book.csv   
example:  
```
st_name,JSTtime,sonde_no
St.4a,2024-06-18_06:01,1101771
```
#### 2.Prepare ```namelist.py```
set ```fbook_path```,```raw_data_dir```,```qc_data_dir```.  
```
fbook_path = "../data/field_book.csv"
raw_data_dir = "../data/raw_data"
qc_data_dir = "../data/qc_data"
```
#### 3. Run QC script.
run ```preprocess.py```.  
post QC data were generated in ```qc_data_dir```.  
field of QC data.  
|TimeUTC|Prs|Tmp|Hum|Height|WD|WS|GeodetLon|GeodetLat|
|----|----|----|----|----|----|----|----|----|
|UTC time|Pressure[hPa]|Temperature[degC]|RH[%]|Height[m]|Wind Direction[deg]|Wind Speed[m/s]|decimal longitude[deg]|decimal latitude[deg]|
### visualization
#### 1. set ```namelist.py``` variables.  
```
fig_dir = "../fig"

# 2D/3D trajectory
plot_area = [136, 138, 34.0, 35.5, -4000, 15000]
# 2D trajectory
lon_ticks = np.arange(135.5, 138.6, 0.5)
lat_ticks = np.arange(34.0, 35.6, 0.5)

# 3D trajectory
azimuth = 240  # 180 : north up
elevation = 25

# 3D trajectory animation
var_name = "rh"
start_time = "2024-06-18_06:00:00"
end_time = "2024-06-18_16:00:00"
frame_delta_min = "10"
plot_delta_min = "20"
```
#### 2. Run ```figure.py```.
- emagram
- 2D trajectory
- 3D trajectory

#### 3. run ```plot_3d_trajectory_animation.py```.
- 3D trajectory animation.  

## Sample_Seisuimaru2407
### radiosonde data  
```sample_Seisuimaru2407/data/raw_data```  
Sample data was observed in Seisui-maru 2407 cruise  
(2024年度　三重大学　陸海空・環境科学実習).  
### field book 
```sample_Seisuimaru2407/data/field_book.csv```   
### script
- ```sample_Seisuimaru2407/libcheck.py```  
check the dependencies.
- ```sample_Seisuimaru2407/preprocess.py```  
conduct quality Control
- ```sample_Seisuimaru2407/figures.py```  
plot emagram and 2D/3D trajectory
- ```sample_Seisuimaru2407/script/plot_3d_trajectory_animation.py```   
plot animation of the 3D trajectories.


## Author
Sou Tomita

