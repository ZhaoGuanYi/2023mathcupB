# Importing required modules
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from model import *
import warnings
warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标题
plt.rcParams['axes.unicode_minus'] = False


def F1(a,b):
    return Z1(a,b)


def F2(a,b):
    return Z2(a, b)


def F3(a,b):
    return Z3(a, b)


# Function to find index of list
# 查找列表指定元素的索引
def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


# Function to sort by values
# 函数根据指定的值列表排序
'''list1=[1,2,3,4,5,6,7,8,9]
   value=[1,5,6,7]
   sort_list=[1,5,6,7]
'''


def sort_by_values(list1, values):
    sorted_list = []
    while (len(sorted_list) != len(list1)):
        # 当结果长度不等于初始长度时，继续循环
        if index_of(min(values), values) in list1:
            # 标定值中最小值在目标列表中时
            sorted_list.append(index_of(min(values), values))
        #     将标定值的最小值的索引追加到结果列表后面
        values[index_of(min(values), values)] = math.inf
    #      将标定值的最小值置为无穷小,即删除原来的最小值,移向下一个
    #     infinited
    return sorted_list


# Function to carry out NSGA-II's fast non dominated sort
# 函数执行NSGA-II的快速非支配排序,将所有的个体都分层
'''
郭军p21
1.np=0 sp=infinite
2.对所有个体进行非支配判断，若p支配q，则将q加入到sp中，并将q的层级提升一级。
  若q支配p，将p加入sq中，并将p的层级提升一级。
3.对种群当前分层序号k进行初始化，令k=1
4.找出种群中np=0的个体，将其从种群中移除，将其加入到分层集合fk中，该集合就是层级为0个体的集合。
5.判断fk是否为空，若不为空，将fk中所有的个体sp中对应的个体层级减去1，且k=k+1,跳到2;
  若为空，则表明得到了所有非支配集合，程序结束
'''
"""基于序列和拥挤距离,这里找到任意两个个体p,q"""


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


# Function to calculate crowding distance
# 计算拥挤距离的函数
'''
高媛p29
1.I[1]=I[l]=inf，I[i]=0 将边界的两个个体拥挤度设为无穷。
2.I=sort(I,m)，基于目标函数m对种群排序
3.I[i]=I[i]+(Im[i+1]-Im[i-1])/(fmax-fmin)
'''


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


#     返回拥挤距离

# 函数进行交叉
def crossover(a, b):
    r = random.random()
    if r > 0.5:
        return mutation((a + b) / 2)
    else:
        return mutation((a - b) / 2)


# 函数进行变异操作
def mutation(solution):
    mutation_prob = random.random()
    if mutation_prob < 1:
        solution = min_fk + (max_fk - min_fk) * random.random()
    return solution


def randm():
    solution = list()
    solution_ = list()
    for i in range(0, pop_size):
        while True:
            x1 = round(min_fk + (max_fk - min_fk) * random.random())
            x2 = round(min_fk + (max_fk - min_fk) * random.random())
            if(x1+x2>25)and(x1/x2%1==0 or x2/x1%1==0):
                solution.append(x1)
                solution_.append(x2)
                break
    return solution, solution_


if __name__ == '__main__':

    pop_size = 100
    max_gen = 10
    # 迭代次数
    # Initialization
    min_fk = 10
    max_fk = 30

    solution, solution_ = randm()
    # 随机生成变量
    gen_no = 0
    while (gen_no < max_gen):
        function1_values = [F1(solution[i], solution_[i]) for i in range(0, pop_size)]
        function2_values = [F2(solution[i], solution_[i]) for i in range(0, pop_size)]
        function3_values = [F3(solution[i], solution_[i]) for i in range(0, pop_size)]
        # 生成两个函数值列表，构成一个种群
        non_dominated_sorted_solution = \
            fast_non_dominated_sort(function1_values[:], function2_values[:], function3_values[:])
        # 种群之间进行快速非支配性排序,得到非支配性排序集合

        tt = list()
        for valuez in non_dominated_sorted_solution[0]:
            # print(round(solution[valuez], 3), end=" ")
            t = [round(solution[valuez], 3), round(solution_[valuez], 3),
                   round(F1(solution[valuez],solution_[valuez]), 3),
                   round(F2(solution[valuez],solution_[valuez]), 3),
                   round(F3(solution[valuez], solution_[valuez]), 3),
                 ]
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
        solution2 = solution[:]
        solution2_ = solution_[:]
        # 生成了子代
        while (len(solution2) != 2 * pop_size):
            a1 = random.randint(0, pop_size - 1)
            b1 = random.randint(0, pop_size - 1)
            # 选择
            solution2.append(crossover(solution[a1], solution[b1]))
            solution2_.append(crossover(solution_[a1], solution_[b1]))
            # 随机选择，将种群中的个体进行交配，得到子代种群2*pop_size

        function1_values2 = [F1(solution2[i], solution2_[i]) for i in range(0, pop_size)]
        function2_values2 = [F2(solution2[i], solution2_[i]) for i in range(0, pop_size)]
        function3_values2 = [F3(solution2[i], solution2_[i]) for i in range(0, pop_size)]
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
        solution = [solution2[i] for i in new_solution]
        solution_= [solution2_[i] for i in new_solution]
        gen_no = gen_no + 1

    # Lets plot the final front now
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    function1 = [-i for i in function1_values]
    function2 = [-i for i in function2_values]
    function3 = [-j for j in function3_values]
    ax.set_xlabel('Z1', fontsize=15)
    ax.set_ylabel('Z2', fontsize=15)
    ax.set_zlabel('Z3', fontsize=15)
    ax.plot(function1,function2,function3,'.',alpha=0.5)
    a = cc  # 顶层
    function11 = [-F1(a[i][0],a[i][1]) for i in range(len(a))]
    function22 = [-F2(a[i][0],a[i][1]) for i in range(len(a))]
    function33 = [-F3(a[i][0],a[i][1]) for i in range(len(a))]
    ax.plot(function11,function22,function33,'r.',alpha=0.5)
    print("顶层解集：",a)
    plt.show()

