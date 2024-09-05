import numpy as np
import pandas as pd
import torch
# from torch.autograd import Variable
# from imblearn.over_sampling import SMOTE
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt
import torch.nn as nn
# !!! Minimizes MSE instead of BCE
adversarial_loss = torch.nn.MSELoss()
from torch.autograd import Variable
Tensor =torch.FloatTensor

Sample = []
gene_name = []
stay_line = ""
real_label = Variable(torch.ones(90))  # 定义真实label为1
fake_label = Variable(torch.zeros(90))
def DownloadM():
    MuteData = []
    #file2 = "data/exchange_row_col_17105.txt"
    file2 = "A.txt"
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
    print(len(Sample))
    #print(gene_name)
    #print((np.array(MuteData)))
    return np.array(MuteData,dtype='float32')

X_for_generate = DownloadM()
X_for_generate=torch.tensor(X_for_generate)
#定义gan模型#############
gene_number= 244
# 超参数
BATCH_SIZE = 1
LR_G = 0.0003          # G生成器的学习率
LR_D = 0.0003          # D判别器的学习率
N_IDEAS = 100            # G生成器的初始想法(随机灵感)

# 搭建G生成器
G = nn.Sequential(                      # 生成器
    # nn.Linear(N_IDEAS, 256),  # 生成器等的随机想法
    # nn.Dropout(0.5),
    # nn.LeakyReLU(0.2),
    #
    # nn.Linear(256, 512),
    # nn.Dropout(0.5),
    # nn.LeakyReLU(0.2),
    #
    # nn.Linear(512, 1024),
    # nn.Dropout(0.5),
    # nn.LeakyReLU(0.2),
    #
    # nn.Linear(1024, gene_number),
    # nn.Softsign(),
    # nn.ReLU(),
    nn.Linear(N_IDEAS, 256),
    nn.Dropout(0.7),
    nn.ReLU(True),


    nn.Linear(256, 512),
nn.Dropout(0.7),
    nn.ReLU(True),


    nn.Linear(512, 1024),
nn.Dropout(0.7),
    nn.ReLU(True),


    nn.Linear(1024, gene_number),
nn.Dropout(0.7),
    # nn.Softsign(),
    # nn.ReLU()
nn.Tanh()

)
# 搭建D判别器
# D = nn.Sequential(                      # 判别器
#     nn.Linear(gene_number, 256),
#     nn.ReLU(),
# #     nn.LeakyReLU(0.2),  # 进行非线性映射
# #     nn.Linear(256, 256),
# #     nn.ReLU(),
#     nn.Linear(256, 1),
#     nn.Sigmoid(),                   # 转换为0-1
# )
D = nn.Sequential(
nn.Linear(gene_number, 1024),
nn.ReLU(True),
nn.Linear(1024, 128),
nn.ReLU(True),
nn.Linear(128, 16),
nn.ReLU(True),
nn.Linear(16, 1),
nn.Sigmoid()
)


# 定义判别器和生成器的优化器
opt_D = torch.optim.Adam(D.parameters(),lr=LR_D)
opt_G = torch.optim.Adam(G.parameters(),lr=LR_G)
#gan模型#############结束

# GAN训练
#print(names[0])
for step in range(5000):
    #lry  after add
    # Adversarial ground truths
    valid = Variable(Tensor(1, 1).fill_(1.0), requires_grad=False)
    fake = Variable(Tensor(1, 1).fill_(0.0), requires_grad=False)
    # 随机选取BATCH个真实的标签为1的样本
    chosen_data = np.random.choice((X_for_generate.shape[0]),size=(BATCH_SIZE),replace=False)
    #print(chosen_data)
    artist_paintings = X_for_generate[chosen_data,:]
    #print(artist_paintings)
    # 使用生成器生成虚假样本

    G_ideas = torch.randn(BATCH_SIZE, N_IDEAS, requires_grad=True)
    G_paintings = G(G_ideas)
    # 使用判别器得到判断的概率
    prob_artist1 = D(G_paintings)
    # 生成器损失
    G_loss = torch.mean(torch.log(1. - prob_artist1))
    #G_loss=criterion(prob_artist1 , fake_label)
    #G_loss=adversarial_loss(prob_artist1, valid)
#         import pdb
#         pdb.set_trace()
    opt_G.zero_grad()
    G_loss.backward()
    opt_G.step()

    prob_artist0 = D(artist_paintings)
    prob_artist1 = D(G_paintings.detach())
    # 判别器的损失
    D_loss = - torch.mean(torch.log(prob_artist0) + torch.log(1. - prob_artist1))
     # Measure discriminator's ability to classify real from generated samples
    #real_loss = adversarial_loss(prob_artist0, valid)
    #fake_loss = adversarial_loss(prob_artist1, fake)
    #D_loss = 0.5 * (real_loss + fake_loss)
    opt_D.zero_grad()
    D_loss.backward(retain_graph=True)
    opt_D.step()
    if step%100==0:
#         print(prob_artist0)
        print(1+G_loss)
        print(D_loss)

def fake_data_save(data):
    data[data >= 0.85] = 1.0
    data[data < 0.85] = 0.0
    data = data.astype(int)
    print(data)
    with open("FakeData_BLCA.txt", 'a+') as f:
        f.truncate(0)
        #print(gene_name[0])
        stay_line = "\t".join(gene_name[0])
        f.write(stay_line+"\n")
        for i in range(0, len(data)):
            s = "BLCA-MN-" + str(i)
            str1 = "\t".join(str(data[i][j]) for j in range(len(data[i])))
            str1 = s + "\t" + str1
            print(str1)
            f.write(str1+"\n")
        print("写入成功")


n_generate = 90

print("------------------")
print(n_generate)
print(N_IDEAS)
fake_data = G(torch.randn(n_generate,N_IDEAS)).detach().numpy()
print(np.max(fake_data,axis=1))
print(np.min(fake_data,axis=1))
fake_data_save(fake_data)
# fake_data=normalize_by_row(fake_data)
# X_default = pd.DataFrame(np.concatenate([X_for_generate,fake_data]),columns=[f'fea{i}' for i in range(1,X_train.shape[1] + 1)])