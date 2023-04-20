import math
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model_v2 import *
import warnings
warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标题
plt.rcParams['axes.unicode_minus'] = False


def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    sorted_list = []
    while len(sorted_list) != len(list1):
        # 当结果长度不等于初始长度时，继续循环
        if index_of(min(values), values) in list1:
            # 标定值中最小值在目标列表中时
            sorted_list.append(index_of(min(values), values))
        #     将标定值的最小值的索引追加到结果列表后面
        values[index_of(min(values), values)] = math.inf
    #      将标定值的最小值置为无穷小,即删除原来的最小值,移向下一个
    #     infinited
    return sorted_list


def fast_non_dominated_sort(values1, values2, values3):
    S = [[] for i in range(0, len(values1))]
    # 种群中所有个体的sp进行初始化 这里的len(value1)=pop_size
    front = [[]]
    # 分层集合,二维列表中包含第n个层中,有那些个体
    n = [0 for i in range(0, len(values1))]
    rank = [0 for i in range(0, len(values1))]
    # 评级

    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        # 寻找第p个个体和其他个体的支配关系
        # 将第p个个体的sp和np初始化
        for q in range(0, len(values1)):
            # step2:p > q 即如果p支配q,则
            if (values1[p] >= values1[q] and values2[p] >= values2[q] and values3[p] >= values3[q])\
                    and not all([values1[p]==values1[q],values2[p] == values2[q],values3[p] == values3[q]]):
                # 支配判定条件:当且仅当,对于任取i属于{1,2},都有fi(p)>fi(q),符合支配.或者当且仅当对于任意i属于{1,2},有fi(p)>=fi(q),且至少存在一个j使得fj(p)>f(q)  符合弱支配
                if q not in S[p]:
                    # 同时如果q不属于sp将其添加到sp中
                    S[p].append(q)
            # 如果q支配p
            elif (values1[q] >= values1[p] and values2[q] >= values2[p] and values3[q] >= values3[p])\
                    and not all([values1[q]==values1[p],values2[q] == values2[p],values3[q] == values3[p]]):
                # 则将np+1
                n[p] = n[p] + 1
        if n[p] == 0:
            # 找出种群中np=0的个体
            rank[p] = 0
            # 将其从pt中移去
            if p not in front[0]:
                # 如果p不在第0层中
                # 将其追加到第0层中
                front[0].append(p)

    i = 0
    while (front[i] != []):
        # 如果分层集合为不为空，
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                # 则将fk中所有给对应的个体np-1
                if (n[q] == 0):
                    # 如果nq==0
                    rank[q] = i + 1

                    if q not in Q:
                        Q.append(q)
        i = i + 1
        # 并且k+1
        front.append(Q)

    del front[len(front) - 1]

    return front
    # 返回将所有个体分层后的结果


def crowding_distance(values1, values2, values3, front):
    distance = [0 for _ in range(0, len(front))]
    # 初始化个体间的拥挤距离
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    sorted3 = sort_by_values(front, values3[:])
    # 基于目标函数1和目标函数2对已经划分好层级的种群排序
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (values1[sorted1[k + 1]] - values1[sorted1[k - 1]]) / (max(values1) - min(values1))
        distance[k] = distance[k] + (values2[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (max(values2) - min(values2))
        distance[k] = distance[k] + (values3[sorted3[k + 1]] - values3[sorted3[k - 1]]) / (max(values3) - min(values3))
    return distance


def crossover(a, b, min, max):
    r = random.random()
    if r > 0.5:
        return mutation((a + b) / 2,min, max)
    else:
        return mutation((a - b) / 2,min, max)


# 函数进行变异操作
def mutation(solution, min, max):
    mutation_prob = random.random()
    if mutation_prob < 1:
        solution = min + (max - min) * random.random()
    return solution


def panduan(sa,sb,a,b):
    flag1 = False
    flag2 = False
    ss = [1,2,5,8,10,14,17,18,21,22,25,26,27,30]
    a_b = sb-sa
    if (sa in ss) and (sb in ss) and 3 <= a_b <= 24:
        flag1 = True
    if (25<a+b<=30) and (a/b % 1 == 0 or b/a % 1 == 0):
        flag2 = True

    return all([flag1,flag2])

def randm():
    solution_a = list()
    solution_b = list()
    solution_sa = list()
    solution_sb = list()
    for i in range(0, pop_size):
        while True:
            x1 = round(min_fk + (max_fk - min_fk) * random.random())
            x2 = round(min_fk + (max_fk - min_fk) * random.random())
            s1 = round(sa_min + (sa_max - sa_min) * random.random())
            s2 = round(sb_min + (sb_max - sb_min) * random.random())
            if panduan(s1,s2,x1,x2):
                solution_a.append(x1)
                solution_b.append(x2)
                solution_sa.append(s1)
                solution_sb.append(s2)
                break
    return solution_a,solution_b,solution_sa,solution_sb


if __name__ == '__main__':

    pop_size = 60
    max_gen = 10
    # 迭代次数
    # Initialization
    min_fk = 10
    max_fk = 16
    sa_min = 1
    sa_max = 6
    sb_min = 22
    sb_max = 30

    solution_a, solution_b,solution_sa,solution_sb = randm()
    # 随机生成变量
    gen_no = 0
    while (gen_no < max_gen):
        function1_values = []
        function2_values = []
        function3_values = []
        ob_list = []
        for i in range(0, pop_size):
            ob = Target(solution_sa[i], solution_sb[i],solution_a[i],solution_b[i])
            ob.build()
            function1_values.append(ob.Z1())
            function2_values.append(ob.Z2())
            function3_values.append(ob.Z3())
            ob_list.append(ob)
        # 生成两个函数值列表，构成一个种群
        non_dominated_sorted_solution = \
            fast_non_dominated_sort(function1_values[:], function2_values[:], function3_values[:])
        # 种群之间进行快速非支配性排序,得到非支配性排序集合

        tt = list()
        for valuez in non_dominated_sorted_solution[0]:
            ob1 = ob_list[valuez]
            t = [solution_sa[valuez], solution_sb[valuez],solution_a[valuez],solution_b[valuez],ob1.Z1(), ob1.Z2(), ob1.Z3()]
            print(t, end=" ")
            tt.append(t)
        print("\n")
        cc = np.array(tt)
        crowding_distance_values = []
        # 计算非支配集合中每个个体的拥挤度
        for i in range(0, len(non_dominated_sorted_solution)):
            crowding_distance_values.append(
                crowding_distance(function1_values[:], function2_values[:],
                                  function3_values[:], non_dominated_sorted_solution[i][:])
            )
        solution2_a = solution_a[:]
        solution2_b = solution_b[:]
        solution2_sa = solution_sa[:]
        solution2_sb = solution_sb[:]
        while (len(solution2_a) != 2 * pop_size):
            a1 = random.randint(0, pop_size - 1)
            b1 = random.randint(0, pop_size - 1)
            # 选择
            aa = round(crossover(solution_a[a1], solution_a[b1],min_fk,max_fk))
            bb = round(crossover(solution_b[a1], solution_b[b1],min_fk,max_fk))
            saa = round(crossover(solution_sa[a1], solution_sa[b1],sa_min,sa_max))
            sbb = round(crossover(solution_sb[a1], solution_sb[b1],sb_min,sb_max))
            if panduan(saa, sbb, aa, bb):
                solution2_a.append(aa)
                solution2_b.append(bb)
                solution2_sa.append(saa)
                solution2_sb.append(sbb)
            # 随机选择，将种群中的个体进行交配，得到子代种群2*pop_size

        function1_values2 = []
        function2_values2 = []
        function3_values2 = []
        for i in range(0, pop_size):
            ob2 = Target(solution2_sa[i], solution2_sb[i], solution2_a[i], solution2_b[i])
            ob2.build()

            function1_values2.append(ob2.Z1())
            function2_values2.append(ob2.Z2())
            function3_values2.append(ob2.Z3())

        non_dominated_sorted_solution2 = \
            fast_non_dominated_sort(function1_values2[:], function2_values2[:], function3_values2[:])
        # 将两个目标函数得到的两个种群值value,再进行排序 得到2*pop_size解

        crowding_distance_values2 = []
        for i in range(0, len(non_dominated_sorted_solution2)):
            crowding_distance_values2.append(
                crowding_distance(function1_values2[:], function2_values2[:],
                                  function3_values2[:], non_dominated_sorted_solution2[i][:]))
        # 计算子代的个体间的距离值
        new_solution = []
        for i in range(0, len(non_dominated_sorted_solution2)):
            non_dominated_sorted_solution2_1 = [
                index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
                range(0, len(non_dominated_sorted_solution2[i]))]
            # 排序
            front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
            front = [non_dominated_sorted_solution2[i][front22[j]] for j in
                     range(0, len(non_dominated_sorted_solution2[i]))]
            front.reverse()  # 反转列表
            for value in front:
                new_solution.append(value)
                if (len(new_solution) == pop_size):
                    break
            if (len(new_solution) == pop_size):
                break
        solution_a = [solution2_a[i] for i in new_solution]
        solution_b= [solution2_b[i] for i in new_solution]
        solution_sa = [solution2_sa[i] for i in new_solution]
        solution_sb = [solution2_sb[i] for i in new_solution]
        gen_no = gen_no + 1

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    function1 = [-i for i in function1_values]
    function2 = [-i for i in function2_values]
    function3 = [-j for j in function3_values]
    ax.set_xlabel('COST1', fontsize=15)
    ax.set_ylabel('COST2', fontsize=15)
    ax.set_zlabel('COST3', fontsize=15)
    ax.plot(function1, function2, function3, '.', alpha=0.5)

    a = np.unique(cc, axis=0)  # 顶层去重
    function11 = [-a[i][4] for i in range(len(a))]
    function22 = [-a[i][5] for i in range(len(a))]
    function33 = [-a[i][6] for i in range(len(a))]
    ax.plot(function11, function22, function33, 'r.', alpha=0.5)
    dd = pd.DataFrame(a)
    dd.to_excel(r"./结果数据表/顶层最优解2.xlsx")
    plt.show()
