import random

import pandas as pd
import numpy as np

###################
# IV类型客流区间
Sa = 5
Sb = 25
N = 30

###################
# 断面客流
fpath1 = r"./Data_B/附件4：断面客流数据.xlsx"
Dm = pd.read_excel(fpath1)
Dm = np.array([0] + list(Dm.iloc[:, 1])+[0])

#####################
# 区间客流
fpath2 = r"./Data_B/附件3：OD客流数据.xlsx"
Quv = pd.read_excel(fpath2)
Quv = np.array(Quv)
Q1, Q2 = 0, 0  # Q2 IV区间流量  Q1 其他区间
for i in range(Sa, Sb):
    for j in range(i + 1, Sb + 1):
        Q2 += Quv[i, j]

for i in range(1, N):
    for j in range(i + 1, N + 1):
        Q1 += Quv[i, j]
Q1 -= Q2

##########################
# 目标函数
# 区间距离
fpath3 = r"./Data_B/附件2：区间运行时间.xlsx"
L = pd.read_excel(fpath3)
Ld = np.array([0] + list(L.iloc[:, 2]))
L1 = sum(Ld)
L2 = sum(Ld[Sa:Sb])


# 企业成本
def Z1(f1, f2):  # 距离函数
    Vm = f1 * L1 + f2 * L2
    return -Vm


def Z2(f1, f2):  # 车辆总量函数
    N = f1 + f2
    return -N


###########################
# 目标函数
tau = 0.04  # 乘客平均上下车时间


# 服务水平

def fuc_tm(m):
    dm1 = 0
    dm2 = 0
    for i in range(m + 1, N + 1):
        dm1 += Quv[m][i]
    for j in range(1, m):
        dm2 += Quv[j][m]
    tm = (dm2 + dm1) * tau / 3600
    return tm


def Z3(f1, f2):
    w1 = Q2 / (2 * (f1 + f2))  # IV客流等待时间
    w2 = Q1 / (2 * f1)  # 非IV客流等待时间

    w31, w32 = 0, 0  # 在车时间
    for i in range(Sa, Sb+1):
        w32 += fuc_tm(i)*Dm[i]
    for j in range(1, N+1):
        w31 += fuc_tm(j)*Dm[j]

    w31 = (w31-w32)/f1
    w32 = w32/(f1+f2)

    return -(w1+w2+w31+w32)





"""
s.t.
①Sa = 5
②Sb = 22
③10<f1<30
④10<f2<30
⑤20<tm/fk<120
⑥f1+f2>max(Dm[a,b]) 46535/1860 (25.01)
⑦f1 >  max(Dm[1,a,b,N])33990/1860 (18.27)
⑧f1,f2属于Z+ f1/f2属于Z+
追踪----
"""
