x={'a':10,'b':20,'c':10,'d':20,'e':10}
a=[]
for i in x.keys():
    a.append(x.get(i))
dict = {}
for key in a:
    dict[key] = dict.get(key, 0) + 1
print(dict)


