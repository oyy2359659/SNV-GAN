import numpy as np
from PIL import Image
from scipy.stats import wasserstein_distance

MuteData = []
a = [1,0,1]
b = [0,1,0]
c = [0,1,1]
d = [1,0,0]

def DownloadM():
    file2 = "data/exchange_row_col_90.txt"
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
                    MuteData.append(results)
                else:
                    stay_line = context
            line = line + 1
    print((np.array(MuteData)).shape)

#def exchange1()
def AC():
    x = np.arccos(a,b)
    y = np.arccos(c,d)
    print(x)
    print(y)

def get_cos_similar(v1: list, v2: list):
    num = float(np.dot(v1, v2))  # 向量点乘
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)  # 求模长的乘积
    return 0.5 + 0.5 * (num / denom) if denom != 0 else 0

def Matrix_Transport_Image():
    n = 0
    while(n<1):
        path = 'image/2022-'
        NUM = 255.0
        arr = np.array(MuteData)
        #获取行数
        col_rand_array = np.arange(arr.shape[1])
        print(col_rand_array)
        #随机打乱
        np.random.shuffle(col_rand_array)
        print(col_rand_array[0:10])
        col_rand = arr[:,col_rand_array[0:10]]
        print(col_rand)
        index = (col_rand == 1.0)
        col_rand[index] = NUM
        imagel = Image.fromarray(col_rand)
        path = path + str(n) +'.jpg'
        #imagel.show()
        #imagel.convert('RGB').save(path)
        n = n + 1

if __name__ == '__main__':
    DownloadM()
    Matrix_Transport_Image()
    #AC()
    # x = wasserstein_distance(a,b)
    # y = wasserstein_distance(c,d)
    # x = get_cos_similar(a,b)
    # y = get_cos_similar(c,d)
    # print(x)
    # print(y)