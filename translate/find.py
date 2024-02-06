from dicfunction import *

#nmode=1 -> number mode /   
nmode=0

letter = []
divide = []

# for문 나중에는 while로 변경. 들어온 input이 없을때까지 반복하기 voule받는거 앞으로 빼는 것도
for i in range(3):
# 첫번째 2차원배열에 만들기
    value=input()
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
# 합성된 것 문자열로 저장해놓기
