# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : data_eda.py
# Time       ：2023/5/19 10:29
# Author     ：author name
# version    ：python 3.6
# Description：
"""
import pandas as pd
import os

import numpy as np
import pandas as pd
import os
from tqdm import tqdm


## 合并同车型数据集
def con_data(path, name):
    data = pd.DataFrame()
    for i in os.listdir(path):
        print(i)
        if i[:4] == name:
            data_i = pd.read_excel(path + '/' + i)
            data = pd.concat([data, data_i])
    data.reset_index(drop=True, inplace=True)
    return data


def charging_energy(start, end, data):
    time_delta = (pd.to_datetime(end) - pd.to_datetime(start)).seconds
    charging_delta = data[(data['数据时间'] >= start) & (data['数据时间'] <= end)]
    sum_energy = (20 / 3600) * abs(sum(charging_delta['总电流']))
    return sum_energy


def charge_no(data):
    # 充电周期
    k = 0
    for i, row in tqdm(data.iterrows()):
        # print(i,row)
        if row['充电状态'] == 1:
            data.loc[i, 'charge_no'] = k
        elif i == len(data) - 1:
            break
        elif row['充电状态'] != 1 and data.loc[i + 1, '充电状态'] == 1:
            k += 1
        else:
            continue
    return data


def need_data(data):
    k = data[data['charge_no'] >= 1]['charge_no'].nunique()
    data_train = pd.DataFrame()
    for i in range(1, k + 1):
        soc_max = data[data['charge_no'] == i]['SOC'].max()
        soc_min = data[data['charge_no'] == i]['SOC'].min()
        li = data[data['charge_no'] == i]['SOC'].tolist()
        if soc_max >= 90 and soc_min <= 40 and 40 in li and 90 in li:
            data_train = pd.concat(
                [data_train, data[(data['charge_no'] == i) & (data['SOC'] >= 40) & (data['SOC'] <= 90)]])
    data_train.reset_index(drop=True, inplace=True)
    return data_train


def train_data(data_train):
    k0 = data_train[data_train['charge_no'] != -1]['charge_no'].unique().tolist()
    values = []
    for i in k0:
        start = data_train[data_train['charge_no'] == i]['数据时间'].min()
        end = data_train[data_train['charge_no'] == i]['数据时间'].max()
        time_delta = (pd.to_datetime(end) - pd.to_datetime(start)).seconds / 20
        # print(time_delta)
        data_len = len(data_train[data_train['charge_no'] == i])
        # print(data_len,time_delta+1)
        ratio = data_len / (time_delta + 1)
        mile = data_train[data_train['charge_no'] == i]['累计里程'].min()
        energy = charging_energy(start, end, data_train[data_train['charge_no'] == i])
        values.append([start, end, ratio, mile, energy])
    return pd.DataFrame(values, columns=['start', 'end', 'ratio', 'mile', 'energy'])


def run(path, name):
    print("====" * 5 + "合并数据中" + "====" * 5)
    all_data = con_data(path, name)
    print("====" * 5 + "增加周期" + "====" * 5)
    charge_data = charge_no(all_data)
    print("====" * 5 + "选择合适的充电段数据" + "====" * 5)
    data_train = need_data(charge_data)
    print("====" * 5 + "输出训练集" + "====" * 5)
    train = train_data(data_train)

    return train


if __name__ == '__main__':
    name_li = ['CL10', 'CL11', 'CL12', 'CL13', 'CL14']
    path = r'C:\code\python\EV\15台车运行数据'
    for i in name_li:
        print(f"正在处理{i}：")
        train_ = run(path, i).to_csv(f'C:/code/python/EV/data/train_all/{i}.csv',index=False)

