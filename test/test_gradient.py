import numpy as np
from dicfunction import *

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

errorrange = 1.2
size=len(dot)
x=[]
y=[]
y_temp=[]

for i in range(size) :
    y_temp.append(dot[i][1])
y_temp.sort
key=y_temp[int(size/4)]

for i in range(size) :
    if dot[i][1]<=key :
        x.append(dot[i][0])
        y.append(dot[i][1])

poly = np.polyfit(x,y,1)

# 각도 구하기 (라디안 단위)
angle_radians = -np.arctan(poly[0])

# 라디안에서 도 단위로 변환
angle_degrees = np.degrees(angle_radians)
# 회전 변환 행렬 계산
rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians)],
                            [np.sin(angle_radians), np.cos(angle_radians)]])

newdot = []

for i in range(size):
    # 회전 변환 적용
    new_x, new_y = np.dot(rotation_matrix, [dot[i][0], dot[i][1]])
    newdot.append([new_x, new_y])

newdot_sorted = sorted(newdot, key=lambda x: x[0])

# for point in newdot_sorted:
#     print(f"({point[0]}, {point[1]})")

x_diff=[]
for i in range(size-1):
    x_diff.append(newdot_sorted[i+1][0]-newdot_sorted[i][0])
x_diff.append(3) #원래는 0인데 if문 돌아가게 하기 위한 조건
x_diff_sorted = sorted(x_diff)

j=0
count=0
group=[]
x_space=[] #공백 크기 구하기 [1]이 점자왼쪽 오른쪽 차이 [2]가 띄어쓰기
while(count<3):
    diff=x_diff_sorted[j+1]-x_diff_sorted[j]
    group.append(x_diff_sorted[j])
    if diff < 2 :
        j+=1
    else:
        x_space.append(sum(group)/len(group))
        count+=1
        group=[]
        j+=1

temp_y=[]
for i in range(size) :
    temp_y.append(newdot_sorted[i][1])

temp_y.sort()
y_range=[]
count=1
y_range.append(temp_y[0])
for i in range(size-1) :
    if temp_y[i+1]-temp_y[i]>3 :
        y_range.append(temp_y[i])
        y_range.append(temp_y[i+1])
y_range.append(temp_y[size-1])

temp=[]
zero=[0,0,0]
line=[0,0,0]
bit_diff=[]
for i in range(size):
    temp.append(newdot_sorted[i])
    if x_diff[i]>2:
        # 같은 세로 줄에 있는 경우
        for j in range(len(temp)):
            if y_range[0] <= temp[j][1] <= y_range[1]:
                line[0] = 1
            elif y_range[2] <= temp[j][1] <= y_range[3]:
                line[1] = 1
            elif y_range[4] <= temp[j][1] <= y_range[5]:
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

bit_array=[]
temp_bit=[]
zero=[0,0,0]
#print(bit_diff)
#첫번째 나오는 오른쪽에 둘지 왼쪽에 둘지 정하기
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
    # for i in range(0, len(bit_array), 3):
    #     print(bit_array[i:i+3])
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
    threebit.append(bit_array.pop(0))
    threebit.append(bit_array.pop(0))
    del bit_array[0]
    bit6 = ''.join(''.join(map(str, sublist)) for sublist in threebit)
    sixbit.append(bit6)
    threebit=[]

if len(bit_array) == 2:
    threebit.append(bit_array.pop(0))
    threebit.append(bit_array.pop(0))
    bit6 = ''.join(''.join(map(str, sublist)) for sublist in threebit)
    sixbit.append(bit6)
    
#6bit변환 시작
#nmode=1 -> number mode /   
nmode=0

letter = []
divide = []

# for문 나중에는 while로 변경. 들어온 input이 없을때까지 반복하기 voule받는거 앞으로 빼는 것도
for i in range(len(sixbit)):
# 첫번째 2차원배열에 만들기
    value=sixbit.pop(0)
    if value=="001001":
         if nmode ==1:
             letter.append([0,0,0,11]) #-땜에 추가
         else:
            letter.append([0,0,0,0])
         #숫자모드에서 001001은 '-' 그래서 이거에 관한 처리하려면 이 경우엔 숫자칸에 -에 해당하는거 만들어서 넣어줘야함
    else:
        if value=="000000":
            nmode=0
            letter.append([0,0,0,0])
            letter.append([0,0,0,0])
        else:
            if nmode==0: 
                if value == "001111":
                    nmode=1
                else:
                    matval=match(value)
                    if len(matval)==2:
                        letter.append(makecol(matval[0],matval[1]))
                    else:
                        #약어인 경우
                        letter.append(makecol(matval[0],matval[1]))
                        letter.append(makecol(matval[2],matval[3]))
            else:
                matval=numget(value)
                #숫자에서 찾음
                if matval == None:
                    nmode=0
                    #숫자에서 나와서 다시 찾아 넣기
                    matval=match(value)
                    if len(matval)==2:
                        letter.append(makecol(matval[0],matval[1]))
                    else:
                        #약어인 경우
                        letter.append(makecol(matval[0],matval[1]))
                        letter.append(makecol(matval[2],matval[3]))
                else:
                    matval = (3,matval)
                    letter.append(makecol(matval[0],matval[1]))
                    # 찾은 숫자열 2차원배열에 넣기
#공백만들기
divide =makespace(letter)


# 띄어쓰기 추가된 array 하나씩 빼내기

i=0
bundle=[] #하나로 합성할 글자
outtext=''
j=0
while len(divide) != 0:
    temp=divide.pop(0)
    # temp는 앞에서부터 하나씩 받아온 것
    #print(temp)
    if temp == [0,0,0,0]:
        if len(bundle) != 0:
            # print(bundle)
            # 한글자로 합성
            outtext=outtext+transasc(bundle)
            j=j+1
            bundle=[]
            # print("합성")
            #합성하면서 bundle비우기
        
    else:
        bundle.append(temp)
        
if len(bundle) != 0:
            # print(bundle)
            # 한글자로 합성
            outtext=outtext+transasc(bundle)
            j=j+1
            bundle=[]
            # print("합성")
            #합성하면서 bundle비우기


print(outtext) 