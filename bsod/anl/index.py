#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


def rm_decending(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    rm_indice = []

    min_p = df["Prs"].iloc[0]
    for i in range(1, len(df)):
        if df["Prs"].iloc[i] >= min_p:
            rm_indice.append(i)
        else:
            min_p = df["Prs"].iloc[i]
    df = df.drop(rm_indice, axis=0).reset_index(drop=True)

    return df
