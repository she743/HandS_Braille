import numpy as np
from dicfunction import *
from find import *

dot = [ [456, 52],
        [438, 51],
        [362, 49],
        [331, 48],
        [240, 46],
        [179, 44],
        [117, 42],
        [67, 41],
        [54, 40],
        [455, 38],
        [35, 40],
        [362, 37],
        [345, 36],
        [314, 35],
        [253, 34],
        [192, 32],
        [130, 30],
        [68, 28],
        [54, 27],
        [439, 26],
        [332, 23],
        [301, 23],
        [240, 21],
        [223, 20],
        [179, 19],
        [161, 19],
        [117, 17],
        [99, 17],
        [68, 15],
        [36, 15]]

def dot2braille(dot):
    errorrange = 2.1 #점간거리, 자간거리인지 구할 때 오차
    errorrange_y = 2.7 # y값 경계 오차 범위 
    errorx = 2.7
    size=len(dot)
    x=[]
    y=[]
    y_temp=[]

    #y좌표 중간값 구하기 : 가장 윗줄 고르기를 점의 갯수를 통해 구하기
    y_temp = sorted([point[1] for point in dot])
    key=y_temp[int(size/4)]

    # key를 기준으로 가장 윗줄의 점 분류
    for i in range(size) :
        if dot[i][1] <= key :
            x.append(dot[i][0])
            y.append(dot[i][1])

    # 점들을 선형 회귀하여 기울기 계산
    poly = np.polyfit(x,y,1)

    # 각도 구하기
    angle_radians = -np.arctan(poly[0])
    rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians)],
                                [np.sin(angle_radians), np.cos(angle_radians)]])

    #회전 후의 점들 계산
    newdot = []
    for i in range(size):
        new_x, new_y = np.dot(rotation_matrix, [dot[i][0], dot[i][1]])
        newdot.append([new_x, new_y])

    #회전 후의 점들을 x좌표로 정렬
    newdot_sorted = sorted(newdot, key=lambda x: x[0])

    #x좌표 차이 계산
    x_diff=[]
    for i in range(size-1):
        x_diff.append(newdot_sorted[i+1][0]-newdot_sorted[i][0])
    x_diff.append(3) #원래는 0인데 if문 돌아가게 하기 위한 조건

    #x좌표 차이값이 점간 거리인지 자간 거리인지 알아내기
    #x_space [1]에 점간거리 [2]에 자간거리를 입력
    x_diff_sorted = sorted(x_diff)
    count=0
    group=[]
    x_space=[]
    for i in range(len(x_diff)-1):
        if count >= 3:
            break
        diff=x_diff_sorted[i+1]-x_diff_sorted[i]
        group.append(x_diff_sorted[i])
        if diff >= errorx :
            x_space.append(sum(group)/len(group))
            count += 1
            group=[]

    #y 좌표 범위 계산
    temp_y = sorted([point[1] for point in newdot_sorted])
    y_range=[temp_y[0]]
    for i in range(size-1) :
        if temp_y[i+1]-temp_y[i] > errorrange_y :
            y_range.extend([temp_y[i],temp_y[i+1]])
    y_range.append(temp_y[size-1])

    #점자 문자 식별

    #점들의 좌표로 같은 세로선에 있는 것들을 식별해 3bit와 다음 세로선과의 거리를 함께 list에 입력
    #다음 세로선과의 거리는 점간거리, 자간거리, 점간거리+자간거리, 더 긴거리로 구분함
    temp=[]
    line=[0,0,0]
    bit_diff=[]
    for i in range(size):
        temp.append(newdot_sorted[i])
        if x_diff[i]>2:        # 같은 세로 줄에 있는 경우 오차범위 부여
            for point in temp:
                if y_range[0] <= point[1] <= y_range[1]:
                    line[0] = 1
                elif y_range[2] <= point[1] <= y_range[3]:
                    line[1] = 1
                elif y_range[4] <= point[1] <= y_range[5]:
                    line[2] = 1
            if x_space[1]-errorrange <= x_diff[i] <= x_space[1]+errorrange:
                num_diff=1
            elif x_space[2]-errorrange <= x_diff[i] <= x_space[2]+errorrange:
                num_diff=2
            elif x_space[1]+x_space[2]-errorrange*2 <= x_diff[i] <= x_space[1]+x_space[2]+errorrange*2:
                num_diff=3
            elif x_diff[i] > x_space[1]+x_space[2]+errorrange*2:
                num_diff=4
            else:
                num_diff=0
            bit_diff.append([line, num_diff])
            line=[0,0,0]
            temp=[]

    #3의 
    bit_array=[]
    temp_bit=[]
    zero=[0,0,0]
    while len(bit_array)==0:
        temp_bit = bit_diff.pop(0)
        if temp_bit[1] == 1:
            bit_array.append(temp_bit[0])
            break
        elif temp_bit[1] == 2:
            bit_array.append(zero)
            bit_array.append(temp_bit[0])
            bit_array.append(zero)
            break
        elif temp_bit[1] == 3:
            for i in range(len(bit_diff)):
                if bit_diff[i][1] == 1:
                    bit_array.append(temp_bit[0])
                    j=1
                    break
                elif bit_diff[i][1] == 2:
                    bit_array.append(zero)
                    bit_array.append(temp_bit[0])
                    bit_array.append(zero)
                    j=1
                    break
                elif bit_diff[i][1] == 4:
                    j=0
                    break
                else :
                    j=0
            if j == 1 :
                break

    j=0
    while bit_diff[0][1]!=0 :
        temp_bit = bit_diff.pop(0)
        bit_array.append(temp_bit[0])
        if temp_bit[1] == 2:
            bit_array.append(zero)
        elif temp_bit[1] == 3:
            bit_array.append(zero)
            bit_array.append(zero)
        elif temp_bit[1] == 4 :
            bit_array.append(zero)
            bit_array.append(zero)
            bit_array.append(zero)
            for i in range(len(bit_diff)) :
                if bit_diff[i][1] == 1:
                    j=1
                    break
                elif bit_diff[i][1] == 2 :
                    j=2
                    break
                elif bit_diff[i][1] == 4 :
                    j=4
                    break
            if j in [1,2] :
                while len(bit_array) % 3 != j-1 :
                    bit_array.append(zero)
            if j == 4:
                break

    bit_array.append(bit_diff[0][0])

    sixbit=[]
    threebit=[]
    #3bit+3bit 행렬을 6bit로 변환
    while len(bit_array)>=3 :
        for _ in range(2):
            threebit.append(bit_array.pop(0))
        del bit_array[0]
        bit6 = ''.join(''.join(map(str, sublist)) for sublist in threebit)
        sixbit.append(bit6)
        threebit=[]

    if len(bit_array) == 2:
        for _ in range(2):
            threebit.append(bit_array.pop(0))
        bit6 = ''.join(''.join(map(str, sublist)) for sublist in threebit)
        sixbit.append(bit6)
    elif len(bit_array) == 1:
        threebit.extend([bit_array.pop(0),[0,0,0]])
        bit6 = ''.join(''.join(map(str, sublist)) for sublist in threebit)
        sixbit.append(bit6)
    return sixbit


braille=dot2braille(dot)
print(translate(braille))