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

## 合并同车型数据集
path = r'E:\data\比赛数据\train'
data = pd.DataFrame()
for i in os.listdir(path):
    print(i)
    if i[:4] == 'CL1_':
        data_i = pd.read_excel(path+'/'+i)
        data = pd.concat([data,data_i,data_i])

k = 0
for i in tqdm(range(len(data))):
    if data.iloc[i]['充电状态'] != 1:
        # data.at[i, '充电周期'] = -1
        continue
    elif data.iloc[i]['充电状态'] == 1 and data.iloc[i - 1]['充电状态'] != 1:
        k += 1
        data.at[i, '充电周期'] = k
    elif data.iloc[i]['充电状态'] == 1 and data.iloc[i - 1]['充电状态'] == 1:
        data.at[i, '充电周期'] = k


def charging_energy(start, end, data):
    time_delta = (pd.to_datetime(end) - pd.to_datetime(start)).seconds
    charging_delta = data[(data['数据时间'] >= start) & (data['数据时间'] <= end)]
    sum_energy = (time_delta / 3600) * abs(sum(charging_delta['总电流']))
    return sum_energy

def encode_data(state,data):
    data['充电状态']==1


if __name__ == '__main__':
    data = pd.read_excel('./CL20_20220701000000_20220731235959.xlsx')
    start = '2022-04-01 03:59:18'
    end = '2022-04-01 03:59:38'
    print(data[(data['数据时间'] >= start)])
    # print(charging_energy('2022-04-01 03:59:18', '2022-04-01 03:59:58', data))
