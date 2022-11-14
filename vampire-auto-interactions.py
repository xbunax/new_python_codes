# Vampire-auto-interactions

"""
这个脚本用于快速生成ucf文件的 Interactions 部分
当前只支持层内J1,J2和J3,暂不支持层间

需要输入的数据在下面的 input 中
    1   x,y,z等同于ucf文件的 unit cell size，用于计算距离判断邻近、次邻近等
    2   coordinate等同于ucf文件的 atoms cx cy cz，同时按照顺序确定了原子编号atoms num
    3   eps是坐标计算误差，因为考虑到x,y,z和coordinate做过近似，用于正确判断等距和邻近、次邻近
    4   n是interaction起始序号，因为现在只能生成层内，所以如果有两层的话就要运行一次后改n和coordinate再运行，例如改成48

如果不需要次邻近或次次邻近，请参考注释说明将指定代码注释掉

结果将输出到脚本文件所在目录下，生成ucf.txt文件
"""

import numpy as np

# input ##------------------------------------------------------------
x, y, z = 6.017, 10.4281, 17.3011  # unit cell size

coordinate = [np.array([0, 0, 0]), np.array([0.5, 0.5, 0]), np.array(
    [0, 0.333, 0]), np.array([0.5, 0.833, 0])]  # 原子坐标，这里的顺序即是原子编号atoms num

eps = 0.05  # 坐标计算误差，判断等距

n = 0  # n是interaction序号起始值
# ---------------------------------------------------------------------


for i in range(len(coordinate)):
    coordinate[i][0] *= x
    coordinate[i][1] *= y
    coordinate[i][2] *= z

atom_num = len(coordinate)

coordinate_l = [np.array(i)+np.array([-x, 0, 0]) for i in coordinate]
coordinate_r = [np.array(i)+np.array([x, 0, 0]) for i in coordinate]
coordinate_u = [np.array(i)+np.array([0, y, 0]) for i in coordinate]
coordinate_d = [np.array(i)+np.array([0, -y, 0]) for i in coordinate]
coordinate_lu = [np.array(i)+np.array([-x, y, 0]) for i in coordinate]
coordinate_ru = [np.array(i)+np.array([x, y, 0]) for i in coordinate]
coordinate_ld = [np.array(i)+np.array([-x, -y, 0]) for i in coordinate]
coordinate_rd = [np.array(i)+np.array([x, -y, 0]) for i in coordinate]

area_dict = {0: "0\t0\t0", 1: "-1\t0\t0", 2: "1\t0\t0", 3: "0\t1\t0",
             4: "0\t-1\t0", 5: "-1\t1\t0", 6: "1\t1\t0", 7: "-1\t-1\t0", 8: "1\t-1\t0"}

coordinates = coordinate+coordinate_l+coordinate_r+coordinate_u + \
    coordinate_d+coordinate_lu+coordinate_ru+coordinate_ld+coordinate_rd


txt = []
for j in range(len(coordinate)):
    atom = coordinate[j]
    distance_dict = dict()
    for i in range(len(coordinates)):
        other_atom = coordinates[i]
        if atom is other_atom:
            continue

        distance = np.linalg.norm(atom-other_atom, 2)
        # print(distance)
        distance_dict.update({i: distance})

    distance_min = min(list(distance_dict.values()))

    ## 邻近，如果不需要直接注释掉这个循环 ##
    for i, distance in distance_dict.items():
        distances_min2 = [i for i in list(
            distance_dict.values()) if (i-distance_min) > eps]
        distance_min2 = min(distances_min2)
        distances_min3 = [i for i in distances_min2 if (i-distance_min2) > eps]
        distance_min3 = min(distances_min3)
        if abs(distance_min-distance) < eps:
            other_atom_index = i % atom_num  # 计算另一个原子的编号
            other_atom_area = area_dict[i//atom_num]
            textline = "{:}\t{:}\t{:}\t{:}\tJ1\n".format(
                n, j, other_atom_index, other_atom_area)
            n += 1
            txt.append(textline)

    ## 次邻近，如果不需要直接注释掉这个循环 ##
    for i, distance in distance_dict.items():
        distances_min2 = [i for i in list(
            distance_dict.values()) if (i-distance_min) > eps]
        distance_min2 = min(distances_min2)
        distances_min3 = [i for i in distances_min2 if (i-distance_min2) > eps]
        distance_min3 = min(distances_min3)
        if abs(distance_min2-distance) < eps:
            other_atom_index = i % atom_num  # 计算另一个原子的编号
            other_atom_area = area_dict[i//atom_num]
            textline = "{:}\t{:}\t{:}\t{:}\tJ2\n".format(
                n, j, other_atom_index, other_atom_area)
            n += 1
            txt.append(textline)

    ## 次次邻近，如果不需要直接注释掉这个循环 ##
    for i, distance in distance_dict.items():
        distances_min2 = [i for i in list(
            distance_dict.values()) if (i-distance_min) > eps]
        distance_min2 = min(distances_min2)
        distances_min3 = [i for i in distances_min2 if (i-distance_min2) > eps]
        distance_min3 = min(distances_min3)
        if abs(distance_min3-distance) < eps:
            other_atom_index = i % atom_num  # 计算另一个原子的编号
            other_atom_area = area_dict[i//atom_num]
            textline = "{:}\t{:}\t{:}\t{:}\tJ3\n".format(
                n, j, other_atom_index, other_atom_area)
            n += 1
            txt.append(textline)

file = open("ucf.txt", "w")
file.writelines(txt)
file.close()
