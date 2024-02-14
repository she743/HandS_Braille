import numpy as np

# Example dot data
# dot = [ [456, 52],
#        [438, 51],
#        [362, 49],
#        [331, 48],
#        [240, 46],
#        [179, 44],
#        [117, 42],
#        [67, 41],
#        [54, 40],
#        [455, 38],
#        [35, 40],
#        [362, 37],
#        [345, 36],
#        [314, 35],
#        [253, 34],
#        [192, 32],
#        [130, 30],
#        [68, 28],
#        [54, 27],
#        [439, 26],
#        [332, 23],
#        [301, 23],
#        [240, 21],
#        [223, 20],
#        [179, 19],
#        [161, 19],
#        [117, 17],
#        [99, 17],
#        [68, 15],
#        [36, 15]]

def dot2braille(dot):
    error_range = 2.1 # Error range to distinguish between whether it is distance between dots characters
    error_range_y = 2.7 #  Error range for y-axis
    error_x = 2.7
    size = len(dot)
    x = []
    y = []
    y_temp = []

    # Calculate y-coordinate for appropriate trendline
    y_temp = sorted([point[1] for point in dot])
    key = y_temp[int(size/4)]

    # Distinguish top line dots accoding to key values
    for i in range(size) :
        if dot[i][1] <= key :
            x.append(dot[i][0])
            y.append(dot[i][1])

    # Calculate slope for trendline
    poly = np.polyfit(x,y,1)

    # Calculate angle and rotation matrix
    angle_radians = -np.arctan(poly[0])
    rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians)],
                                [np.sin(angle_radians), np.cos(angle_radians)]])

    # Calculate coordinate after rotation of image
    newdot = []
    for i in range(size):
        new_x, new_y = np.dot(rotation_matrix, [dot[i][0], dot[i][1]])
        newdot.append([new_x, new_y])

    # Sort dots in ascending order of x-coordinates
    newdot_sorted = sorted(newdot, key=lambda x: x[0])

    # Calculate difference bewteen x-coordinates
    x_diff=[]
    for i in range(size-1):
        x_diff.append(newdot_sorted[i+1][0] - newdot_sorted[i][0])
    x_diff.append(3) # Added to prevent error occurence

    # Distinguish whether x-coordinate difference is distance bewteen dots or characters
    # Insert distance between dots to x_space[1] and [2] for characters
    x_diff_sorted = sorted(x_diff)
    count = 0
    group = []
    x_space = []
    for i in range(len(x_diff)-1):
        if count >= 3:
            break
        diff = x_diff_sorted[i+1] - x_diff_sorted[i]
        group.append(x_diff_sorted[i])
        if diff >= error_x :
            x_space.append(sum(group)/len(group))
            count += 1
            group = []

    # Calculate y-coodrinate range
    temp_y = sorted([point[1] for point in newdot_sorted])
    y_range = [temp_y[0]]
    for i in range(size-1) :
        if temp_y[i+1]-temp_y[i] > error_range_y :
            y_range.extend([temp_y[i], temp_y[i+1]])
    y_range.append(temp_y[size-1])

    # Start analysis
    # Append values of x-coordinate on one vertical line (upto 3 dots),
    # and the distance between given vertical line and the next vertical line

    # Get distance between given vertical line and the next line by comparing and getting the largest value of
    # distance between dots, distance between characters, and the sum of the two

    temp = []
    line = [0,0,0]
    bit_diff = []
    for i in range(size):
        temp.append(newdot_sorted[i])
        if x_diff[i] > 2:
            for point in temp:
                if y_range[0] <= point[1] <= y_range[1]:
                    line[0] = 1
                elif y_range[2] <= point[1] <= y_range[3]:
                    line[1] = 1
                elif y_range[4] <= point[1] <= y_range[5]:
                    line[2] = 1
            if x_space[1] - error_range <= x_diff[i] <= x_space[1] + error_range:
                num_diff = 1
            elif x_space[2] - error_range <= x_diff[i] <= x_space[2] + error_range:
                num_diff = 2
            elif x_space[1] + x_space[2] - error_range*2 <= x_diff[i] <= x_space[1] + x_space[2] + error_range*2:
                num_diff = 3
            elif x_diff[i] > x_space[1] + x_space[2] + error_range*2:
                num_diff = 4
            else:
                num_diff = 0
            bit_diff.append([line, num_diff])
            line = [0,0,0]
            temp = []

    # Distinguish braille dot positions according to remainder of 3
    bit_array = []
    temp_bit = []
    zero = [0,0,0]
    while len(bit_array) == 0:
        temp_bit = bit_diff.pop(0)
        if temp_bit[1] == 1:
            bit_array.append(temp_bit[0])
            break
        elif temp_bit[1] == 2:
            bit_array.extend([zero, temp_bit[0], zero])
            break
        elif temp_bit[1] == 3:
            for i in range(len(bit_diff)):
                if bit_diff[i][1] == 1:
                    bit_array.append(temp_bit[0])
                    j = 1
                    break
                elif bit_diff[i][1] == 2:
                    bit_array.extend([zero, temp_bit[0], zero])
                    j = 1
                    break
                elif bit_diff[i][1] == 4:
                    j = 0
                    break
                else :
                    j = 0
            if j == 1 :
                break

    j = 0
    while bit_diff[0][1] != 0 :
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
                    j = 1
                    break
                elif bit_diff[i][1] == 2 :
                    j = 2
                    break
                elif bit_diff[i][1] == 4 :
                    j = 4
                    break
            if j in [1,2] :
                while len(bit_array) % 3 != j-1 :
                    bit_array.append(zero)
            if j == 4:
                break

    bit_array.append(bit_diff[0][0])

    sixbit = []
    threebit = []

    # Transform 3bit+3bit matrix to 6-bit
    while len(bit_array) >= 3 :
        for _ in range(2):
            threebit.append(bit_array.pop(0))
        del bit_array[0]
        bit6 = ''.join(''.join(map(str, sublist)) for sublist in threebit)
        sixbit.append(bit6)
        threebit = []

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

#braille = dot2braille(dot)
#print(translate(braille))