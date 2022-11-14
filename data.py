import numpy
import re
import matplotlib.pyplot as plt
def file(a):
    data_list=[]
    with open(a, 'r') as f:
        for i in f.readlines():
            data_list.append(i)
    return data_list
def filename(V,Vp,N,t,mu):
    return "U4_V{}_Vp{}_tp_N{}_be{}_s1234567_mu{}.tdm.out".format(V,Vp,N,t,mu)
a='/Users/xbunax/Documents/dqmc/check/Pd_data.txt'
data=file(a)
Ls = [48, 64, 80, 96, 112, 128, 144, 160]
dtaus = [0.0625 for i in range(len(Ls))]
density_mu=[[] for i in range(len(Ls))]
T=[]
V=0.3
Vp=0.75
N=36
mu=[-0.09,-0.09,-0.09,-0.08,-0.08,-0.07,-0.07,-0.07]
Pd=[]
Pderr=[]
Pd0=[]
Pd0err=[]
for i in range(len(Ls)):
    T.append(Ls[i]*dtaus[i])
for i in range(len(Ls)):
    density_mu[i].append(T[i])
    density_mu[i].append(mu[i])
for i in range(len(density_mu)):
    for j in range(len(data)):
        if filename(V,Vp,N,density_mu[i][0],density_mu[i][1]) in data[j]:
            print(data[j])
            p=re.findall(r"\d+\.?\d*",data[j])
            n=re.findall(r"-\d+\.?\d*",data[j])
            Pd.append(float(p[9]))
            Pderr.append(float(p[11])*10**float(n[1]))
            Pd0.append(float(p[13]))
            Pd0err.append(float(p[15])*10**float(n[2]))
plt.errorbar(T,Pd,yerr=Pderr,fmt='-co')
plt.show()
plt.errorbar(T,Pd0,yerr=Pd0err)
plt.show()




