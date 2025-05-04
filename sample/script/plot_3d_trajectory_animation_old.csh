#!/usr/bin/csh

###---ここから追加---#### (20250501)
## conda本体を使えるようにする
#source `conda info --base`/etc/profile.d/conda.csh
#
## 仮想環境名が存在するかチェック
#if ($?CONDA_DEFAULT_ENV) then
#    echo "仮想環境 '$CONDA_DEFAULT_ENV' を再アクティベートします。"
#    conda activate $CONDA_DEFAULT_ENV
#else
#    echo "仮想環境はアクティブではありません。conda activate はスキップします。"
##endif

# ここからPythonスクリプト実行
###---ここまで追加---###


# plot 3D trajectory animation

set var_name = "rh"
set start_time = "2024-06-18_06:00:00"
set end_time = "2024-06-18_16:00:00"
<<<<<<< HEAD
set frame_delta_min = "10"
set plot_delta_min = "30"
=======
set frame_delta_min = "30"
set plot_delta_min = "60"
>>>>>>> develop
set fig_dir = "../fig/trajectory3d_animation/${var_name}"

mkdir -p "${fig_dir}/frame"
rm -rf "${fig_dir}/frame/*"

# plot frames
echo "plot frames" 
python3 __frame_3d_trajectory.py \
    $var_name  $start_time $end_time $frame_delta_min $plot_delta_min \
    "${fig_dir}/frame" 

# gif
echo "make GIF"
convert -delay 30 -loop 0 "${fig_dir}/frame/*png" "${fig_dir}/${var_name}.gif"

echo "finish"