# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ProcessData as pd
import os.path as op

Mute = []
Gname = []
dic = {}
dic_Mute = {}
FinalJH = []
FG = []
Gxlist = []

def FG_GL():
    with open("processdata/Dic_Mute.txt", 'r',encoding="utf-8") as f:
        while True:
            context = f.readline().strip('\n')
            if len(context) == 0:
                break
            else:
                l = context.split("\t")
                size = len(l)
                dic_Mute[l[0]] = list(map(float, l[1:size]))

    #print(dic_Mute)
    with open("processdata/JH.txt", 'r',encoding="utf-8") as f:
        line = 1
        while True:
            context = f.readline().strip('\n')
            #print(context)
            if len(context) == 0:
                break
            else:
                JH = context.split("\t")
                #print(JH[0][0])
                if JH[0][0] == "第":
                    continue
                #print(JH)
                c = [0 for i in range(len(Mute[1])-1)]
                size = len(JH)
                for i in range(len(JH)):
                    a = dic_Mute[JH[i]]
                    c = [a[i] or c[i] for i in range(len(a))]
                    #print(c)
                CDsum = float(sum(c))
                # print(CDsum)
                CD = float(CDsum / (len(Mute[1])-1))
                # print(l[1:size])
                if  CDsum > 30:
                    FG.append(CDsum)
                    FinalJH.append(JH)
            line = line + 1
    print(len(FinalJH))
    with open("processdata/FG.txt", 'a+',encoding="utf-8") as f:
        f.truncate(0)
        for i in range(0, len(FinalJH)):
            str1 = "\t".join(FinalJH[i])
            #print("第{}个集合：".format(n))
            #print(str)
            f.write(str1 + "\n")




def ZX():
    p = 0  # 当前正在聚类的第p个集合
    q = 0  # 不合适第p集合的其他基因放入第q集合
    K = [[] for i in range(len(Gname))]
    dist1 = [[] for i in range(len(Gname))]
    Kname = [[] for i in range(len(Gname))]
    size = len(Mute[1])
    with open("processdata/Dic_Mute.txt", 'a+',encoding="utf-8") as f:
        f.truncate(0)
        for i in range(0, len(Gname)):
            dic[Gname[i]] = 0
            dic_Mute[Mute[i][0]] = Mute[i][1:size]
            str1 = "\t".join(Mute[i])
            # print("第{}个集合：".format(n))
            # print(str)
            f.write(str1 + "\n")
    n = 0
    for i in range(0, len(Mute)):  # 循环找
        flag = 0
        if dic[Mute[i][0]] == 1:
            continue
        else:
            Gxname = Mute[i][0]
            Gx = list(map(float, Mute[i][1:size]))
            Gxlist.append(Gx)
            K[p].append(Gx)
            Kname[p].append(Gxname)
            dic[Gxname] = 1
            print("\n正在聚类第{}个集合：".format(p))
            print("{}".format(Gxname), end=",")
            best_dist = 0.1
            for j in range(0, len(Mute)):
                # if dic[Mute[j][0]] == 1:
                #     continue
                if dic[Mute[j][0]] == Gxname:
                    continue
                Gy = list(map(float, Mute[j][1:size]))
                Gyname = Mute[j][0]
                Gz = list(map(lambda a_b: a_b[0] * a_b[1], zip(Gx, Gy)))
                if sum(Gz) == 0:
                    if sum(Gy) > 0:
                        K[p].append(Gy)
                        Kname[p].append(Gyname)
                        #dic[Gyname] = 1
                        print(Gyname, end="(0),")
                        Gx = list(map(lambda a_b: a_b[0] + a_b[1], zip(Gx, Gy)))
                        Gxlist.append(Gx)
                if sum(Gz) != 0:
                    x1 = 1
                    Gzx = list(map(lambda a_b: a_b[0] + a_b[1], zip(Gx, Gy)))
                    Fm = sum(i > 0 for i in Gzx)
                    Fg = sum(Gzx)
                    ED =  Fm/Fg
                    # ED = 2*Fm - Fg
                    dist = ED
                    # print("基因{}与质心的dist={}".format(Gyname,dist))
                    if dist > best_dist:
                        K[p].append(Gy)
                        Kname[p].append(Gyname)
                        #dic[Gyname] = 1
                        best_dist = dist
                        dist1[p].append(dist)
                        Gx = list(map(lambda a_b: a_b[0] + a_b[1], zip(Gx, Gy)))
                        Gxlist.append(Gx)
                        print(Gyname, end="(1), ")

            p = p + 1
    print(p)
    #print(Gxlist)
    n = 1
    #存结果
    with open("processdata/Big_JH.txt", 'a+',encoding="utf-8") as f:
        f.truncate(0)
        for i in range(0, len(Kname)):
            f.write("第"+str(i)+"个集合：" + "\n")
            str2 = "\t".join(Kname[i])
            f.write(str2 + "\n")
    with open("processdata/JH.txt", 'a+',encoding="utf-8") as f1:
        f1.truncate(0)
        for i in range(0, len(Kname)):
            if len(Kname[i]) > 2:
                f1.write("第" + str(n) + "个集合：" + "\n")
                str1 = "\t".join(Kname[i])
                # print("第{}个集合：".format(n))
                # print(str1)
                n = n + 1
                f1.write(str1 + "\n")
    m = 1
    with open("processdata/Big_JHXQ.txt", 'a+',encoding="utf-8") as f1:
        f1.truncate(0)
        for i in range(0, len(Kname)):
            f1.write("第个"+str(i)+"集合：" + "\n")
            for j in range(0, len(Kname[i])):
                str1 = "\t".join(dic_Mute[Kname[i][j]])
            f1.write(str1 + "\n")
    with open("processdata/JHXQ.txt", 'a+',encoding="utf-8") as f:
        f.truncate(0)
        for i in range(0, len(Kname)):
            f.write("第个" + str(m) + "集合：" + "\n")
            for j in range(0, len(Kname[i])):
                str1 = "\t".join(dic_Mute[Kname[i][j]])
                # print(str1)
                if len(Kname[i]) > 2:
                    f.write(str1 + "\n")
            m = m + 1
    with open("processdata/GxList.txt", 'a+',encoding="utf-8") as f:
        f.truncate(0)
        for i in range(0, len(Gxlist)):
            listG = list(map(str, Gxlist[i]))
            str1 = "\t".join(listG)
            f.write(str1 + "\n")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Mute, Gname = pd.Gene_Sort()
    # Mute, Gname = pd.Processing("test.txt")
    # print(Mute)
    ZX()
    #FG_GL()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
