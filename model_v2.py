import pandas as pd
import numpy as np


class Target:
    def __init__(self,Sa,Sb,f1,f2):
        self.Sa = Sa
        self.Sb = Sb
        self.f1 = f1
        self.f2 = f2
        self.N = 30
        self.L1 = 0
        self.L2 = 0
        self.Q1 = 0
        self.Q2 = 0
        self.Quv = []
        self.Dm = []
        self.tau = 0.04  # 乘客平均上下车时间

    def build(self):
        # 断面客流
        fpath1 = r"./Data_B/附件4：断面客流数据.xlsx"
        Dm = pd.read_excel(fpath1)
        Dm = np.array([0] + list(Dm.iloc[:, 1]) + [0])
        self.Dm = Dm

        # 区间客流
        fpath2 = r"./Data_B/附件3：OD客流数据.xlsx"
        Quv = pd.read_excel(fpath2)
        Quv = np.array(Quv)
        self.Quv = Quv
        Q1, Q2 = 0, 0  # Q2 IV区间流量  Q1 其他区间
        for i in range(self.Sa, self.Sb):
            for j in range(i + 1, self.Sb + 1):
                Q2 += Quv[i, j]

        for i in range(1, self.N):
            for j in range(i + 1, self.N + 1):
                Q1 += Quv[i, j]
        Q1 -= Q2

        self.Q1 = Q1
        self.Q2 = Q2

        # 区间距离
        fpath3 = r"./Data_B/附件2：区间运行时间.xlsx"
        L = pd.read_excel(fpath3)
        Ld = np.array([0] + list(L.iloc[:, 2]))
        L1 = sum(Ld)
        L2 = 0
        for i in range(self.Sa, self.Sb):
            L2 += Ld[i]
        self.L1 = L1
        self.L2 = L2

    def Z1(self):
        Vm = self.f1 * self.L1 + self.f2 * self.L2
        return -Vm

    def Z2(self):
        n = self.f1 + self.f2
        return -n

    def fuc_tm(self,m):
        dm1 = 0
        dm2 = 0
        for i in range(m + 1, self.N + 1):
            dm1 += self.Quv[m][i]
        for j in range(1, m):
            dm2 += self.Quv[j][m]
        tm = (dm2 + dm1) * self.tau / 3600
        return tm

    def Z3(self):
        w1 = self.Q2 / (2 * (self.f1 + self.f2))  # IV客流等待时间
        w2 = self.Q1 / (2 * self.f1)  # 非IV客流等待时间
        w31, w32 = 0, 0  # 在车时间
        for i in range(self.Sa, self.Sb + 1):
            w32 += self.fuc_tm(i) * self.Dm[i]
        for j in range(1, self.N + 1):
            w31 += self.fuc_tm(j) * self.Dm[j]

        w31 = (w31 - w32) / self.f1
        w32 = w32 / (self.f1 + self.f2)

        return -(w1 + w2 + w31 + w32)

