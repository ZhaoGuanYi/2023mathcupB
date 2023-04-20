import numpy as np
import pandas as pd

from model import *
import datetime
import math

ccc = [fuc_tm(i)*3600 for i in range(1, 30)]

path = r"./Data_B/附件2：区间运行时间.xlsx"
b = pd.read_excel(path)
b = list(b.iloc[:, 1])
a = []
f = 13
c = 0


for i in range(1, 30):
    aa = fuc_tm(i) * 3600
    if Sa < i < Sb:
        aa1 = aa/(2*f)
    else:
        aa1 = aa/f
    if aa1>20:
        c+=1
    a.append(aa1)

ccc = pd.DataFrame(a)
# ccc.to_excel("./停站时间.xlsx")

start = datetime.datetime(1,1,1,hour=7)
start1 = 0
start2 = start
print("第一站发车时间", start)


# step = datetime.timedelta(seconds=round(3600/f))
step2 = datetime.timedelta(seconds=round(1800/f))
step = 2*step2

time_arr = [['']*33 for _ in range(60)]
for z in range(1, f+1):
    n = 1
    idx = n
    time_arr[idx][2*z-1] = str(start)[-7:]
    for i, j in zip(a, b):
        n += 1
        idx += 1
        # 运行时间
        start += datetime.timedelta(seconds=j)
        print(f"{n}到站 {start} 运行时间{j}s")
        time_arr[idx][2*z-1] = str(start)[-7:]

        # 停车间隔
        if i<20:
            start += datetime.timedelta(seconds=20)
        else:
            start += datetime.timedelta(seconds=math.ceil(i))
        print(f"{n}出发 {start} 等待时间{i}s")
        idx += 1
        time_arr[idx][2*z-1] = str(start)[-7:]
        if n == Sa:
            start1 = start
            idx1 = idx

    start1 = start1-step2
    print(f"\n小交发车时间5站{start1}")
    n = Sa
    idx = idx1

    time_arr[idx][2*z] = str(start1)[-7:]
    for i,j in zip(a[Sa-1:Sb-1],b[Sa-1:Sb-1]):
        n += 1
        idx += 1

        # 运行时间
        start1 += datetime.timedelta(seconds=j)
        print(f"{n}到站 {start1} 运行时间{j}s")
        time_arr[idx][2*z] = str(start1)[-7:]
        # 停车间隔
        if i<20:
            start1 += datetime.timedelta(seconds=20)
        else:
            start1 += datetime.timedelta(seconds=math.ceil(i))
        print(f"{n}出发 {start1} 等待时间{i}s")
        idx += 1
        time_arr[idx][2*z] = str(start1)[-7:]

    start = start2 + step
    start2 = start

dp = pd.DataFrame(time_arr)
ff = r"./时刻表3.xlsx"
dp.to_excel(ff)
xx=1