import numpy as np



def DownloadM(path):
    Sample = []
    gene_name = []
    stay_line = ""
    MuteData = []
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
                    Sample.append(l[0])
                    MuteData.append(results)
                else:
                    stay_line = context.split("\t")
                    gene_name.append(stay_line)
            line = line + 1
    #print(len(Sample))
    #print(gene_name)
    #print((np.array(MuteData)))
    return np.array(MuteData,dtype='float32'), Sample, gene_name, stay_line