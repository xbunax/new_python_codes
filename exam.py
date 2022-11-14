a=207
b=[]
k=0
while a!=495:
    b=[]
    for i in str(a):
        b.append(i)
    start=sorted(b)
    s=int(start[0])*100+int(start[1])*10+int(start[2])
    end=sorted(b,reverse=True)
    e=int(end[0])*100+int(end[1])*10+int(end[2])
    a=e-s
    print(a)


