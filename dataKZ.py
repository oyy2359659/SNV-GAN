import numpy as np
import pandas as pd
import torch

Sample = []
gene_name = []

def DownloadReal(path):
    realData = []
    #file2 = "data/exchange_row_col_17105.txt"
    file2 = path#"data/1/BLCA_1data-1.txt"
    # file2 = "data/test.txt"
    with open(file2, 'r') as f:
        line = 0
        while True:
            context = f.readline().strip('\n')
            if len(context) == 0:
                break
            else:
                if line != 0:
                    l = context.split("\t")
                    size = len(l)
                    results = list(map(float, l[1:size]))
                    Sample.append(l[0])
                    realData.append(results)
                else:
                    stay_line = context.split("\t")
                    gene_name.append(stay_line)
            line = line + 1
    print(len(Sample))
    #print(gene_name)
    #print((np.array(MuteData)))
    return realData

def Downloadfake(path):
    fakeData = []
    #file2 = "data/exchange_row_col_17105.txt"
    file2 = path
    # file2 = "data/test.txt"
    with open(file2, 'r') as f:
        line = 0
        while True:
            context = f.readline().strip('\n')
            if len(context) == 0:
                break
            else:
                if line != 0:
                    l = context.split("\t")
                    size = len(l)
                    results = list(map(float, l[1:size]))
                    #Sample.append(l[0])
                    fakeData.append(results)
                else:
                    stay_line = context.split("\t")
            line = line + 1
    #print(gene_name)
    #print((np.array(MuteData)))
    return fakeData

def data_save(real,fake):
    with open("processdata/BLCA_KZdata.txt", 'a+') as f:
        f.truncate(0)
        #print(gene_name[0])
        stay_line = "\t".join(gene_name[0])
        f.write(stay_line+"\n")
        n = 1
        for i in range(0, len(real)):
            s = str(n)
            str1 = "\t".join(str(real[i][j]) for j in range(len(real[i])))
            str1 = s + "\t" + str1
            n = n + 1
            print(str1)
            f.write(str1+"\n")
        Fsize = 489 - len(real)
        print(Fsize)
        arr = np.array(fake)
        # 获取行数
        col_rand_array = np.arange(arr.shape[0])
        print(len(col_rand_array))
        # 随机打乱
        np.random.shuffle(col_rand_array)
        print(col_rand_array[0:Fsize])
        fakerand = col_rand_array[0:Fsize]
        print(len(fakerand))
        print(len(fake))
        for i in range(0, Fsize):
            s = str(n)
            str1 = "\t".join(str(fake[fakerand[i]][j]) for j in range(len(fake[fakerand[i]])))
            str1 = s + "\t" + str1
            n = n + 1
            #print(str1)
            f.write(str1+"\n")
        print("写入成功")

fakedata = Downloadfake("data/1/FakeData_BLCA.txt")
realdata = DownloadReal("data/1/BLCA_1data-1.txt")
data_save(realdata,fakedata)