
def fake_data_save(data, clear, gene_name, savepath, Gnum):
    data[data >= 0.85] = 1.0
    data[data < 0.85] = 0.0
    data = data.astype(int)
    print(data.shape)
    l = len(data)
    n = 0
    if Gnum == 394:
        return Gnum;
    with open(savepath, 'a+') as f:
        if clear == 1:
            f.truncate(0)
            stay_line = "\t".join(gene_name[0])
            f.write(stay_line + "\n")
        #print(gene_name[0])
        #for i in range(l):
            #print("data[{}] = {}".format(i,data[i]))
        for i in range(l):
            #print("data[{}] = ".format(i))
            s = "BLCA-MN-" + str(Gnum)
            #print(data)
            str1 = "\t".join(str(data[i][j]) for j in range(len(data[i])))
            str1 = s + "\t" + str1
            #print(str1)
            f.write(str1 + "\n")
        print("写入成功") 
    return Gnum

# def fake_data_save(data, clear, gene_name, savepath, Gnum):
#     data[data >= 0.85] = 1.0
#     data[data < 0.85] = 0.0
#     data = data.astype(int)
#     print(data)
#     with open(savepath, 'a+') as f:
#         if clear == 1:
#             f.truncate(0)
#         #print(gene_name[0])
#         stay_line = "\t".join(gene_name[0])
#         f.write(stay_line+"\n")
#         for i in range(0, len(data)):
#             s = "BLCA-MN-" + str(i)
#             str1 = "\t".join(str(data[i][j]) for j in range(len(data[i])))
#             str1 = s + "\t" + str1
#             print(str1)
#             f.write(str1+"\n")
#         print("写入成功")