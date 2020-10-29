#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:42:15 2020

@author: susmitvengurlekar
"""

import pandas as pd


df = pd.read_csv("../raw_data/train.csv")

df = df.drop(["ID","Age","Net Sales"],axis=1)
df = df[df["Duration"]>0]

df = df.reset_index()
df = df.drop("index",axis=1)

agency_top = df.groupby(["Agency"])["Claim"].mean().sort_values(ascending=False)[:5].index
agency_map = {j:i for i,j in enumerate(agency_top,1)}
agency_mapping = {}
for unique in df["Agency"].unique():
    if unique in agency_map:
        agency_mapping[unique] = agency_map.get(unique)
    else:
        agency_mapping[unique] = 6
df["Agency"] = df["Agency"].map(agency_mapping)

def is_premium_plan(plan):
    parts = plan.split(" ")
    identifiers = ["Gold","Silver","Platinum","Bronze"]
    for part in parts:
        if part in identifiers:
            return 1
    return 0
    
df["Premium_Plan"] = df["Product Name"].map(is_premium_plan)

prod_name_top = df.groupby(["Product Name"])["Claim"].mean().sort_values(ascending=False)[:10].index
prod_name_map = {j:i for i,j in enumerate(prod_name_top,1)}
prod_name_mappping = {}
for unique in df["Product Name"].unique():
    if unique in prod_name_map:
        prod_name_mappping[unique] = prod_name_map.get(unique)
    else:
        prod_name_mappping[unique] = 11
df["Product Name"] = df["Product Name"].map(prod_name_mappping)

def get_duration_category(d):
    if d < 25:
        return "Short"
    elif d < 200:
        return "Medium"
    elif d < 750:
        return "Long"
    return "Very Long"

df["Duration_Category"] = df["Duration"].map(get_duration_category)

for dur_cat in ["Short","Medium","Long","Very Long"]:
    subset = df[df["Duration_Category"] == dur_cat]
    X = subset["Duration"]
    mean = X.mean()
    std = X.std()
    dur = (X-mean)/std
    df.loc[subset.index,"Duration"] = dur

duration_category_mapper = {
    "Long" : 3,
    "Medium" : 2,
    "Short" : 1,
    "Very Long": 4
}

df["Duration_Category"] = df["Duration_Category"].map(duration_category_mapper)
df["Duration_Time_Cat"] = df["Duration"]**2 * df["Duration_Category"]

dest_top = list(df["Destination"].value_counts()[:14].index)
dest_map = {j:i for i,j in enumerate(dest_top,1)}
dest_mapping = {}
for unique in df["Destination"].unique():
    if unique in dest_map:
        dest_mapping[unique] = dest_map.get(unique)
    else:
        dest_mapping[unique] = 15
        
df["Destination"] = df["Destination"].map(dest_mapping)

df.to_csv("../intermediate_data/pre_processed.csv",index=False)