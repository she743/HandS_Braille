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


def makespace(biglist):
    outlist = []
    blank = [0,0,0,0]

    while(len(biglist)>1) :
        print(len(biglist))
        firstlist=biglist.pop(0)
        secondlist=biglist[0]
        a=checkf(firstlist)
        b=checkf(secondlist)
        print (a, b)
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


def transasc(inplist):
    i=0
    count=0
    count1=0
    if(inplist[0][3]!=0) : #숫자인지 확인
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
        while(inplist[i][1]!=0) : #모음 개수 count
            count=count + 1
            i=i+1
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
       