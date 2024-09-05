import os
import math
import sys
import time

GeneSort = {}
NewMute = []
SortMute = []
MuteDate = []
Genename = []
stay_line = ""
Sort = {}

def BubbleSort(data):
    len_data = len(data)
    size = len(data[0])
    for i in range(1, len_data):
        flag = 0  # 用于标记本次for循环是否曾经有交换动作。如果没有，说明已经排序完成，算法可以提前终止
        for j in range(len_data - i):
            a = sum(list(map(float, data[j][1:size])))
            b = sum(list(map(float, data[j + 1][1:size])))
            if a < b:
                flag = 1
                data[j], data[j + 1] = data[j + 1], data[j]
        if flag == 0:
            return data
    return data


def readline_count(file_name):
    return len(open(file_name).readlines())

def S():
    with open("processdata/NewMute.txt", 'a+') as f:
        f.truncate(0)
        f.write(stay_line)
        for i in range(0, len(NewMute)):
            str = "\t".join(NewMute[i])
            f.write(str+"\n")
        print("写入成功")


def Save(Arr):
    with open("processdata/GBM.txt", 'a+') as f:
        f.truncate(0)
        f.write(stay_line)
        for i in range(0, len(Arr)):
            str = "\t".join(Arr[i])
            f.write(str+"\n")
        print("写入成功")

def Gene_Sort():
    file = "data/MaxMIF-sort.txt"
    ls = readline_count(file)
    with open(file, 'r') as f:
        print("****************正在按照排序删除基因************************")
        line = 0
        start = time.perf_counter()
        while True:
            context = f.readline().strip('\n')
            if len(context) == 0:
                break
            else:
                Ranknum = 1120-56
                if line != 0:
                    l = context.split('\t')
                    if int(l[0]) < Ranknum:
                        GeneSort[l[1]] = int(l[0])
                        Sort[int(l[0])] = l[1]
                    else:
                        GeneSort[l[1]] = 0
            dur = int(time.perf_counter() - start)
            print("\r", end="")
            print("Download progress: {}%       {}s: ".format(line * 100 / ls,dur), "▋" * (int(100 * line / ls) // 2), end="")
            sys.stdout.flush()
            line = line + 1
    file2 = "data/exchange_row_col_90.txt"
    #file2 = "data/test.txt"
    del1num = 0
    del2num = 0
    with open(file2, 'r') as f:
        print("\n********************正在删除覆盖样本低的基因*************************")
        line = 0
        while True:
            context = f.readline().strip('\n')
            if len(context) == 0:
                break
            else:
                if line != 0:
                    l = context.split("\t")
                    size = len(l)
                    #print(size)
                    # print(l[1:size])
                    results = list(map(float, l[1:size]))
                    if l[0] in GeneSort:
                        if GeneSort[l[0]] > 0:
                            if sum(results) > 0:
                                NewMute.append(l)
                                Genename.append(l[0])
                            else:
                                del1num = del1num + 1
                                #print("{}因为覆盖样本不足被删除".format(l[0]))
                        else:
                            del2num = del2num + 1
                            #print("{}排名倒数5%".format(l[0]))
                else:
                    stay_line = context
            line = line + 1
        print("*********************删除覆盖样本低的基因完成******************")
        print(del1num)
        print(del2num)
    S()
    n = 0
    MuteDate = BubbleSort(NewMute)
    # for i in range(1,len(Sort)+1):
    #     Gname = Sort[i]
    #     #print(Gname)
    #     for j in range(len(NewMute)):
    #         if NewMute[j][0] == Gname:
    #             #print(NewMute[j][0])
    #             n = n + 1
    #             MuteDate.append(NewMute[j])
    #             #print(MuteDate)
    #             break
    print(n)
    Save(MuteDate)
    return MuteDate, Genename



