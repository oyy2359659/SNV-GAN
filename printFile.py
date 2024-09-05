def PrintFile(n):
    Gene = []
    with open("processdata/JH.txt", 'r',encoding="utf-8") as f:
        line = 1
        while True:
            context = f.readline().strip('\n')
            # print(context)
            if len(context) == 0:
                break
            else:
                JH = context.split("\t")
                # print(JH[0][0])
                if JH[0][0] == "第":
                    continue
                size = len(JH)
                Gene.append(JH)
            line = line + 1
        for i in range(0,len(Gene[n])):
            print(Gene[n][i])

PrintFile(0)