from dictionary_and_functions import *

def translate(sixbit):
    # Translate 6 bit to string
    # nmode = 1 -> number mode /
    nmode = 0

    letter = []
    divide = []

    # Loop over given list
    for i in range(len(sixbit)):
        value = sixbit.pop(0)

        if value == "001001":
            if nmode == 1:
                letter.append([0,0,0,11]) # added for " - "
            else:
                letter.append([0,0,0,0])
            # 001001 in number -> '-'

        else:
            if value == "000000":
                nmode = 0
                letter.append([0,0,0,0])
                letter.append([0,0,0,0])
            else:
                if nmode == 0:
                    if value == "001111":
                        nmode = 1
                    else:
                        matchval = match(value)
                        if len(matchval) == 2:
                            letter.append(makecol(matchval[0],matchval[1]))
                        else:
                            # In case of abbreviation
                            letter.append(makecol(matchval[0],matchval[1]))
                            letter.append(makecol(matchval[2],matchval[3]))
                else:
                    matval = numget(value)

                    if matval == None:
                        nmode = 0
                        matval = match(value)
                        if len(matval)==2:
                            letter.append(makecol(matval[0],matval[1]))
                        else:
                            # In case for abbreviation
                            letter.append(makecol(matval[0],matval[1]))
                            letter.append(makecol(matval[2],matval[3]))
                    else:
                        matval = (3,matval)
                        letter.append(makecol(matval[0],matval[1]))

    # Add 'space' for translation
    divide = makespace(letter)

    # Translate given final list
    i = 0
    bundle = [] # Initiate variable
    outtext = ''
    j = 0

    while len(divide) != 0:
        temp = divide.pop(0) # get values from the start

        if temp == [0,0,0,0]:
            if len(bundle) != 0:
                # Merge as a 'character'
                outtext = outtext + transasc(bundle)
                j = j+1
                bundle = [] # empty given bundle

        else:
            bundle.append(temp)

    if len(bundle) != 0:
                # Merge as a 'character'
                outtext = outtext + transasc(bundle)
                j = j+1
                bundle = [] # empty given bundle

    return outtext