import pandas as pd
import matplotlib.pyplot as plt
f = r"./Data_B/附件4：断面客流数据.xlsx"

a = pd.read_excel(f)
data = a.iloc[:,1]
x_lim = range(1,30)

plt.scatter(x_lim[5:8],data[5:8],marker='^',c='r')
plt.plot(x_lim,data,'-o')


plt.show()
x=1
