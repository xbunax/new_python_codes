import pexpect
from pathlib import Path
import os

class data_analysis(object):

    def __init__(self):
        self.passwd_key = '12345'
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
            child.expect(pexpect.EOF, timeout=120)  # timeout是持续时间如果下载时间很长可以大一点
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
    def mkdir(self,path,V1_value,V2s_value):#创建文件夹
        Path=path+'/'+str(V1_value)+'_'+str(V2s_value)
        folder = os.path.exists(Path)
        if not folder:
            os.makedirs(Path)
            return Path
        else:
            return Path



    def filename_U4(self, V1_value, V2s_value, Nsite=16, seed='s1234567', number=0.4):
        return "U4_V{}_tp{}_N{}_be4.0_{}_mu-{}.out".format(V1_value, V2s_value, Nsite, seed, number)

    def filename_local_orb(self, V1_value, V2s_value, Nsite=16, seed='s1234567', number=0.4):
        return "local_orb_U4_V{}_tp{}_N{}_be4.0_{}_mu-{}".format(V1_value, V2s_value, Nsite, seed, number)

    def filename_U4_tdm(self, V1_value, V2s_value, Nsite=16, seed='s1234567', number=0.4):
        return "U4_V{}_tp{}_N{}_be4.0_{}_mu-{}.tdm.out".format(V1_value, V2s_value, Nsite, seed, number)
    def filename_geom(self,V1_value,V2s_value,Nsite=16):
        return "geomU4_V{}_tp{}_N{}".format(V1_value,V2s_value,Nsite)

data = data_analysis()
path = '/Users/xbunax/Documents/dqmc'  # 文件夹地址
V1_value = 0.05
V2s_value = 0.01
path1=data.mkdir(path,V1_value,V2s_value)
##分别是ip,用户名,下载文件地址,本地地址
filename_judge = data.filename_U4(V1_value, V2s_value, 16, 's1234567', 0.4)  # U4文件名
filename_local_orb = data.filename_local_orb(V1_value, V2s_value, 16, 's1234567', 0.4)  # local_orb文件名
filename_geo=data.filename_geom(V1_value,V2s_value)
filename_tdm=data.filename_U4_tdm(V1_value,V2s_value)
path3=path1+'/'+'test'
if data.exit(path3, filename_judge) == True and data.exit(path3,filename_local_orb)==True and data.exit(path3,filename_geo)==True and data.exit(path3,filename_tdm)==True:
    data.data_write(path1,'result','=============================')
    data.data_write(path1,'result','Avg and Density')
    data.data_out(path1,path3 + '/' + filename_judge,'Avg',1, 47)
    data.data_out(path1,path3 + '/' + filename_judge,'Density',1, 47)
    data.data_write(path1,'result','local_orb')
    strs=['11','22','33','44','55','66']
    for k in strs:
        data.data_out_local(path1,path3+'/'+filename_local_orb,k,23,59)
    data.data_write(path1,'result','Hamilt')
    data.data_out(path1,path3+'/'+filename_geo,'',17,35)
    data.data_write(path1,'result','tdm_out')
    data.data_out(path1,path3+'/'+filename_tdm,'Pd',44730,44746)
else:
    data.download('10.10.8.74','zhumo','/home/zhumo/run_Ce3PtIn11/test',Path1)
    Path2=path1+'/'+'test'
    data.data_write(path1,'result','Hamilt')
    data.data_out(path1,Path2 + '/' + filename_judge, 'Avg', 1, 47)
    data.data_out(path1,Path2 + '/' + filename_judge, 'Density', 1, 47)
    data.data_write(path1,'result','local_orb')
    strs = ['11', '22', '33', '44', '55', '66']
    for k in strs:
        data.data_out_local(path1,Path2 + '/' + filename_local_orb,k, 23, 59)
    data.data_write(path1,'result','Hamilt')
    data.data_out(path1,Path2 + '/' + filename_geo, '', 17, 35)
    data.data_write(path1,'result','tdm_out')
    data.data_out(path1,Path2 + '/' + filename_tdm, 'Pd', 44730, 44746)













