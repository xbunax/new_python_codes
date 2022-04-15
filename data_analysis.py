import pexpect
from pathlib import Path
import os
import matplotlib.pyplot as plt
import re

class data_analysis(object):

    def __init__(self):
        self.passwd_key = '12345'#密码
        print("data_analysis Working")

    def upload(self, ip, user, dst_path, filename):
        # 上传
        cmdline = 'scp -r %s %s@%s:%s' % (filename, user, ip, dst_path)
        try:
            child = pexpect.spawn(cmdline)
            child.expect(self.passwd_key)
            child.sendline()
            child.expect(pexpect.EOF)
            print("file upload Finish!")
        except Exception as e:
            print("upload failed:", e)

    def download(self, ip, user, dst_path, filename):
        # 下载
        cmdline = 'scp -r %s@%s:%s %s' % (user, ip, dst_path, filename)
        try:
            child = pexpect.spawn(cmdline)
            child.expect("password")
            child.sendline(self.passwd_key)
            child.expect(pexpect.EOF, timeout=None)  #timeout是持续时间如果下载时间很长可以大一点
            print("file download Finish!")
        except Exception as e:
            print("download failed:", e)

    def exit(self, path, filename):#判断文件是否存在
        p = Path(path)
        if p.is_dir() == True:
            files = p.glob(filename)
            if len(list(files)) == 0:
                print('dont exit')
                return False
            else:
                print('exit')
                return True
        else:
            print("this isn't a dir")

    def data_write(self,path,filename,data):
        with open(path+'/'+filename+'.txt','a+') as f:
            f.writelines(data+'\n')
        print('write success')

    def data_out(self, path,filename, strs, numstart,numend):#输出结果
        data_list=[]
        a=[]
        b=[]
        with open(filename, 'r') as f:
            for i in f.readlines():
                data_list.append(i)
        for i in range(numstart,numend):
                k =data_list[i]
                result = "".join(k.split())
                a.append(result)
        for j in range(len(a)):
            if strs in a[j]:
                data_analysis.data_write(self,path,'result',data_list[j+numstart])
                b.append(data_list[j+numstart])
        return b

    def data_out_local(self,path,filename, strs, numstart,numend):#local_orb文件结果输出
        data_list=[]
        a=[]
        b=[]
        with open(filename, 'r') as f:
            for i in f.readlines():
                data_list.append(i)
        for i in range(numstart,numend):
                k =data_list[i]
                result = "".join(k.split())
                a.append(result)
        for j in range(len(a)):
            if str(a[j]).startswith(strs)==True :
                data_analysis.data_write(self,path,'result',data_list[j+numstart])


    def data_tdm_out(self,path,filename,strs):
        data_list=[]
        a=[]
        with open(filename, 'r') as f:
            for i in f.readlines():
                data_list.append(i)
        for i in range(len(data_list)):
                k =data_list[i]
                result = "".join(k.split())
                a.append(result)
        for j in range(len(a)):
            if str(a[j]).startswith(strs)==True:
                for o in range(15):
                    data_analysis.data_write(self,path,'result',data_list[j+o])
                break


    def mkdir(self,path,V1_value,V2s_value,Nsite):#创建文件夹
        Path=path+'/'+str(V1_value)+'_'+str(V2s_value)+'_'+str(Nsite)
        folder = os.path.exists(Path)
        if not folder:
            os.makedirs(Path)
            return Path
        else:
            return Path



    def filename_U4(self, V1_value, V2s_value, Nsite, seed, T,number):
        return "U4_V{}_tp{}_N{}_be{}_{}_mu-{}.out".format(V1_value, V2s_value, Nsite, T,seed, number)

    def filename_local_orb(self, V1_value, V2s_value, Nsite, seed,T,number):
        return "local_orb_U4_V{}_tp{}_N{}_be{}_{}_mu-{}".format(V1_value, V2s_value, Nsite, T,seed, number)

    def filename_U4_tdm(self, V1_value, V2s_value, Nsite, seed,T, number):
        return "U4_V{}_tp{}_N{}_be{}_{}_mu-{}.tdm.out".format(V1_value, V2s_value, Nsite,T,seed, number)

    def filename_geom(self,V1_value,V2s_value,Nsite):
        return "geomU4_V{}_tp{}_N{}".format(V1_value,V2s_value,Nsite)

    def data_conclusion(self,path,V1_value,V2s_value,Nsite,seed,T,number):
        filename_judge = data_analysis.filename_U4(self,V1_value, V2s_value, Nsite, seed, T,number)  # U4文件名
        filename_local_orb = data_analysis.filename_local_orb(self,V1_value, V2s_value, Nsite, seed, T,number)  # local_orb文件名
        filename_geo = data_analysis.filename_geom(self,V1_value, V2s_value, Nsite)
        filename_tdm = data_analysis.filename_U4_tdm(self,V1_value, V2s_value, Nsite,seed,T,number)
        path1 = data_analysis.mkdir(self,path, V1_value, V2s_value, Nsite)  # 创建文件夹返回路径
        path3=path1+'/'+'test'
        if data_analysis.exit(self,path3, filename_judge) == True and data_analysis.exit(self,path3, filename_local_orb) == True and data_analysis.exit(self,path3, filename_geo) == True and data_analysis.exit(self,path3, filename_tdm) == True:
            data_analysis.data_write(self,path1, 'result', '=============================')
            data_analysis.data_write(self,path1, 'result', 'Avg and Density')
            data_analysis.data_out(self,path1, path3 + '/' + filename_judge, 'Avg', 1, 47)
            data_analysis.data_out(self,path1, path3 + '/' + filename_judge, 'Density', 1, 47)
            data_analysis.data_write(self,path1, 'result', 'local_orb')
            strs = ['11', '22', '33', '44', '55', '66']
            for k in strs:
                data_analysis.data_out_local(self,path1, path3 + '/' + filename_local_orb, k, 23, 59)
            data_analysis.data_write(self,path1, 'result', 'Hamilt')
            data_analysis.data_out(self,path1, path3 + '/' + filename_geo, '', 17, 35)
            data_analysis.data_write(self,path1, 'result', 'tdm_out')
            data_analysis.data_tdm_out(self,path1, path3 + '/' + filename_tdm, 'Pd')
        else:
            data_analysis.download(self,'10.10.8.74', 'zhumo', '/home/zhumo/run_Ce3PtIn11/test', path1)
            Path2 = path1 + '/' + 'test'
            data_analysis.data_write(self,path1, 'result', '=============================')
            data_analysis.data_write(self,path1, 'result', 'Hamilt')
            data_analysis.data_out(self,path1, Path2 + '/' + filename_judge, 'Avg', 1, 47)
            data_analysis.data_out(self,path1, Path2 + '/' + filename_judge, 'Density', 1, 47)
            data_analysis.data_write(self,path1, 'result', 'local_orb')
            strs = ['11', '22', '33', '44', '55', '66']
            for k in strs:
                data_analysis.data_out_local(self,path1, Path2 + '/' + filename_local_orb, k, 23, 59)
            data_analysis.data_write(self,path1, 'result', 'Hamilt')
            data_analysis.data_out(self,path1, Path2 + '/' + filename_geo, '', 17, 35)
            data_analysis.data_write(self,path1, 'result', 'tdm_out')
            data_analysis.data_tdm_out(self,path1, path3 + '/' + filename_tdm, 'Pd')
        return 'Finish'

    def data_temperature(self,path,ls,dtaus,V1_value,V2s_value,Nstie,seed,number):
        b=[]
        l=[]
        y=[]
        err=[]
        for i in range(len(ls)):
            b.append(ls[i]*dtaus[i])
        path1 = data_analysis.mkdir(self, path, V1_value, V2s_value, Nsite)  # 创建文件夹返回路径
        path3 = path1 + '/' + 'test'
        for k in b:
            filename_judge=data_analysis.filename_U4(self,V1_value,V2s_value,Nsite,seed,k,number)
            if data_analysis.exit(self,path3,filename_judge)==True:
                print('exit',filename_judge)
            else:
                print("don't exit:",filename_judge)
            l.append(data_analysis.data_out(self,path3,path3+'/'+filename_judge,'XXAFstructurefactor',47,77))
        for i in l:
            p=re.findall(r"\d+\.?\d*",i[0])
            negative_p=re.findall(r"-\d+\.?\d*",i[0])
            y.append(float(p[0])*10**float(p[1]))
            err.append(float(p[2])*10**float(negative_p[0]))
        plt.errorbar(b,y,yerr=err,fmt='co')
        plt.ylim(0.36,0.375)
        plt.show()





path = '/Users/xbunax/Documents/dqmc'  # 文件夹地址
V1_value = 4.0
V2s_value = 1.0
Ncell=6
Nsite=Ncell**2
ls=[40]
dtaus=[0.1]
#T=ls*dtaus
seed='s1234567'
number=0.4
#data_analysis.data_conclusion(data_analysis,path,V1_value,V2s_value,Nsite,seed,T,number)
data_analysis.data_temperature(data_analysis,path,ls,dtaus,V1_value,V2s_value,Nsite,seed,number)













