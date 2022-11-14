import matplotlib.pyplot as plt
import re
import os
import pexpect
import time
from pexpect import pxssh

path = "/Users/xbunax/Documents/Document/SoftwareOfSpintronics/vampire"#文件本地存储地址
dst_path = "/home/mozhu/vampire-develop/output"#服务器文件地址
password='1171218417'#ssh密码
usr='mozhu'
ip='10.30.13.120'

def download(ip, user, dst_path, filename,password):
    cmdline = 'scp %s@%s:%s %s' % (user, ip, dst_path, filename)  # 10.30.13.120
    print(cmdline)
    try:
        child = pexpect.spawn(cmdline)
        child.expect(".*assword.*")

        child.sendline(password)
        child.expect(pexpect.EOF, timeout=300)        # timeout是持续时间如果下载时间很长可以大一点
        print("file download Finish!")

    except Exception as e:
        print("download failed:", e)

def upload(user, ip, filename, dst_path, password):
    cmdline = 'scp %s %s@%s:%s' % (user, ip, dst_path, filename)  # 10.30.13.120
    print(cmdline)
    try:
        child = pexpect.spawn(cmdline)
        child.expect(".*assword.*")

        child.sendline(password)
        child.expect(pexpect.EOF, timeout=300)  # timeout是持续时间如果上传时间很长可以大一点
        print("file download Finish!")

    except Exception as e:
        print("download failed:", e)


def mkdir(path, filename):#创建文件夹分类存储
    path1 = path + '/' + filename
    folder = os.path.exists(path1)
    if not folder:
        os.makedirs(path1)
        return path1
    else:
        return path1


def read(path):
    a = []
    data = []
    with open(path, 'r') as f:
        for i in f.readlines():
            a.append(i)
    for i in range(8, len(a)):
        k = a[i]
        result = k.split()
        data.append(result)
    return data


def plotfigure(file_path):
    x=[]
    y=[]
    save = read(file_path)
    for i in save:
        x.append(float(i[0]))
        y.append(float(i[5]))

    print(x)
    print(y)
    plt.figure()
    plt.plot(x, y, '-')
    plt.xlabel('T')
    plt.ylabel('magent')
    plt.show()

def ssh(usr,ip,password):
    try:
        PROMPT = ['$', '~']
        s = pxssh.pxssh()
        s.login(ip, usr, password)
        print('success')
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)
    return s

def runtask(child):
    child.prompt()
    child.sendline('cd vampire-develop')
    child.prompt()
    # child.sendline('runtask')
    # child.prompt()
    child.sendline('qstat')
    child.prompt()
    i=len(child.before)
    while i!=7:
        child.sendline('qstat')
        child.prompt()
        time.sleep(5)
        print(child.before)
        i=len(child.before)
    return True

Path=mkdir(path,'test9')
child=ssh(usr, ip ,password)
if runtask(child)==True:
    download(ip, usr, dst_path, Path,password)
    plotfigure(Path+'/'+'output')

