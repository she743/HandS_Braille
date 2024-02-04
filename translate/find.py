dicstart = {
"000100" : 1, #초성 ㄱ
"100100" : 3, #초성 ㄴ
"010100" : 4, #초성 ㄷ
"000010" : 6, #초성 ㄹ
"100010" : 7, #초성 ㅁ
"000110" : 8, #초성 ㅂ
"000001" : 10, #초성 ㅅ
"000101" : 13, #초성 ㅈ
"000011" : 15, #초성 ㅊ
"110100" : 16, #초성 ㅋ
"110010" : 17, #초성 ㅌ
"100110" : 18, #초성 ㅍ
"010110" : 19 #초성 ㅎ
}

dicmid = {
"110001" : 1, #모음 ㅏ
"001110" : 3, #모음 ㅑ
"011100" : 5, #모음 ㅓ
"100011" : 7, #모음 ㅕ
"101001" : 9, #모음 ㅗ
"001101" : 13, #모음 ㅛ
"101100" : 14, #모음 ㅜ
"100101" : 18, #모음 ㅠ
"010101" : 19, #모음 ㅡ
"101010" : 21, #모음 ㅣ
"111010" : 2, #모음 ㅐ
"101110" : 6, #모음 ㅔ
"001100" : 8, #모음 ㅖ
"111001" : 10, #모음 ㅘ
"101111" : 12, #모음 ㅚ
"111100" : 15, #모음 ㅝ
"010111" : 20 #모음 ㅢ
}

dicend = {
"100000" : 2, #종성 ㄱ
"010010" : 5, #종성 ㄴ
"001010" : 8, #종성 ㄷ
"010000" : 9, #종성 ㄹ
"010001" : 17, #종성 ㅁ
"110000" : 18, #종성 ㅂ
"001000" : 20, #종성 ㅅ
"011011" : 22, #종성 ㅇ
"101000" : 23, #종성 ㅈ
"011000" : 24, #종성 ㅊ
"011010" : 25, #종성 ㅋ
"011001" : 26, #종성 ㅌ
"010011" : 27, #종성 ㅍ
"001011" : 28  #종성 ㅎ
}

dicabb = {
"110101" : [0,1,1,1],  #약어 가
"111000" : [0,10,1,1],  #약어 사
"100111" : [1,5,2,2],  #약어 억
"011111" : [1,5,2,5],  #약어 언
"011110" : [1,5,2,9],  #약어 얼
"100001" : [1,7,2,5],  #약어 연
"110011" : [1,7,2,9],  #약어 열
"110111" : [1,7,2,22],  #약어 영
"101101" : [1,9,2,2],  #약어 옥
"111011" : [1,9,2,5], #약어 온
"111111" : [1,9,2,22], #약어 옹
"110110" : [1,14,2,5], #약어 운
"111101" : [1,14,2,9], #약어 울
"101011" : [1,19,2,5], #약어 은
"011101" : [1,19,2,9], #약어 을
"111110" : [1,21,2,5]  #약어 인
}

dicnum = {
"010110" : 10, #숫자 0
"100000" : 1, #숫자 1
"110000" : 2, #숫자 2
"100100" : 3, #숫자 3
"100110" : 4, #숫자 4
"100010" : 5, #숫자 5
"110100" : 6, #숫자 6
"110110" : 7, #숫자 7
"110010" : 8, #숫자 8
"010100" : 9,  #숫자 9
"001001" : 11 # -
}

# 띄어쓰기 000000

# 6bit 받으면 해당 문자로 변환
def match(bit):
    num=dicstart.get(bit)
    if num != None:
        # 초성에 있는 경우, 입력되는 열 번호는 나중에 처리
        return 0, num
    else:
        num=dicmid.get(bit)
        if num != None:
            #중성에 있는 경우
            return 1, num
        else:
            num=dicend.get(bit)
            if num !=None:
                #종성에 있는 경우
                return 2, num
            else:
                num=dicabb.get(bit)
                if num !=None:
                    # 약어에 있는 경우
                    return num
                else:
                #여기도 없을 때 return 값?일단 7넣음
                    return 7

#make a column for 2D array
def makecol(row, num):
    line =[]
    for j in range(4):
        if j==row:
            line.append(num)
        else:
            line.append(0)
    return line

def checkf(list):
    if list[0]!=0:  #초성 부분인지 확인
        return 0
    elif list[1]!=0: #모음 부분인지 확인
        return 1
    elif list[2]!=0: #종성 부분인지 확인
        return 2
    elif list[3]!=0: #숫자 부분인지 확인
        return 3
    else:            #빈칸인지 확인
        return 4

#공백만들기
def makespace(biglist):
    outlist = []
    blank = [0,0,0,0]

    while(len(biglist)>1) :
        #print(len(biglist))
        firstlist=biglist.pop(0)
        secondlist=biglist[0]
        a=checkf(firstlist)
        b=checkf(secondlist)
        #print (a, b)
        if a==4 or b==4 : #앞이나 뒤가 공백이면
            outlist.append(firstlist)
        elif a==3 or b==3: #앞이나 뒤가 숫자이면
            outlist.append(firstlist)
            outlist.append(blank)
        elif b==2 : #뒤가 종성이면
            outlist.append(firstlist)
        elif a==2 : #앞이 종성이면
            outlist.append(firstlist)
            outlist.append(blank)
        elif a==1 : #앞이 모음이면
            if secondlist[1]==2 or secondlist[1]==8 : #뒤가 ㅐ,ㅖ이면
                outlist.append(firstlist)
            else :
                outlist.append(firstlist)
                outlist.append(blank)
        elif b==0 : #뒤가 초성이면
            if firstlist[0]==10 : #앞이 ㅅ이면
                outlist.append(firstlist)
            else :
                outlist.append(firstlist)
                outlist.append(blank)
        elif a==0 and b==1 :
            outlist.append(firstlist)
        else :
            outlist.append(blank)
    outlist.append(biglist[0])
    
    return outlist

def mixend(key) : 
    telecom = { 202 : 3 , 
                220 : 4 , 
                523 : 6 , 
                528 : 7 , 
                902 : 10 , 
                917 : 11 , 
                918 : 12 , 
                920 : 13 , 
                926 : 14 , 
                927 : 15 , 
                928 : 16 , 
                1820 : 19 }.get(key)
    return telecom

#한글자로 만들기
def transasc(inplist):
    i=0
    count=0
    count1=0
    if(inplist[0][3]!=0) : #숫자인지 확인
        if inplist[0][3]==11:
            return "-" #추가한것 확인필요 - 땜에 추가
        else:
            return str(inplist[0][3]%10)
    else : #글자모드
        if(inplist[0][0]==0) : #초성이 없으면
            num1=12
        elif(inplist[0][0]==10 and inplist[1][0]!=0) : # ㅅ뒤에 다른 초성이 있으면
            num1=inplist[1][0]+1
            i=2
        else :
            num1=inplist[0][0]
            i=1
        while(i<len(inplist)) : #모음 개수 count
            if inplist[i][1] != 0:
                count=count + 1
                i=i+1
            else:
                break
        if(count==0) :
            num2=1
        elif(count==1) :
            num2=inplist[i-1][1]
        elif(count==2) :
            if(inplist[i-1][1]==2) : #두번째 모음이 ㅐ인 경우
                if(inplist[i-2][1]==14) : #우인 경우만 +3
                    num2=inplist[i-2][1]+3
                else : 
                    num2=inplist[i-2][1]+1
            elif(inplist[i-1][1]==8) : #두번째 모음이 ㅖ인 경우
                num2=inplist[i-2][1]
                num3=21
            else :
                print("오류")
        elif(count==3) :
            if(inplist[i-3][1]==14) :
                num2=inplist[i-3][1]+3
            else :
                num2=inplist[i-3][1]+1
            num3=21
        else :
            print("오류")
        while(i<len(inplist)) : #종성 개수 count
            count1=count1+1
            i=i+1
        if(count1==0) : 
            num3=1
        elif(count1==1) :
            num3=inplist[i-1][2]
        elif(count1==2) :
            num3=mixend(inplist[i-2][2]*100+inplist[i-1][2])
        else :
            print("오류")
        return chr(((num1-1)*21+num2-1)*28+num3-1+0xAC00)


#nmode=1 -> number mode /   
nmode=0

letter = []
divide = []
# for문 나중에는 while로 변경. 들어온 input이 없을때까지 반복하기 voule받는거 앞으로 빼는 것도
for i in range(4):
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
                        #우애넣었을때 여기서 에러가 남
                        letter.append(makecol(matval[0],matval[1]))
                    else:
                        #약어인 경우
                        letter.append(makecol(matval[0],matval[1]))
                        letter.append(makecol(matval[2],matval[3]))
            else:
                matval=dicnum.get(value)
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
while len(divide) != 0:
    temp=divide.pop(0)
    # temp는 앞에서부터 하나씩 받아온 것
    #print(temp)
    if temp == [0,0,0,0]:
        if len(bundle) != 0:
            print(bundle)
            # 한글자로 합성
            print(transasc(bundle))
            bundle=[]
            print("합성")
            #합성하면서 bundle비우기
        
    else:
        bundle.append(temp)
        
if len(bundle) != 0:
            print(bundle)
            # 한글자로 합성
            print(transasc(bundle))
            bundle=[]
            print("합성")
            #합성하면서 bundle비우기

# 합성된 것 문자열로 저장해놓기
