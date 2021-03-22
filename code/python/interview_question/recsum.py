# 1 2 1 2 1 2 1 2
# 1 2 1 2 1 2 1 2
# 1 2 1 2 1 2 1 2
# 1 2 1 2 1 2 1 2
# 1 2 1 2 1 2 1 2
# 1 2 1 2 1 2 1 2
# 
#

#
# [0, 0, 0, 0, 0, 0, 0, 0, 0]
# [0, 1, 3, 4, 6, 7, 9, 10, 12]
# [0, 12, 28, 46, 68, 92, 120, 150, 184]
# [0, 33, 95, 190, 326, 513, 747, 1038, 1394]

# [0, 1, 4, 8, 14]
# [0, 13, 44]

X = 3
Y = 5
img = [
    [1,2,3,4,5],
    [6,7,8,9,10],
    [11,12,13,14,15],
]

def get_integral_img(img, X, Y):
    rowsum_img = [[0]*(Y+1)]
    for i in range(1, X + 1):
        row = [0]
        for j in range(1, Y + 1):
            row.append(row[j-1] + img[i-1][j-1])
        rowsum_img.append(row)

    integral_img = [[0]*(Y+1)]
    for i in range(1, X + 1):
        row = [0]
        for j in range(1, Y + 1):
            #print(i, j)
            #print(rowsum_img[i][j-1])
            #print(integral_img[i-1][j])
            #print(img[i-1][j-1])
            #print('---')
            row.append(rowsum_img[i][j-1] + integral_img[i-1][j] + img[i-1][j-1])
        integral_img.append(row)
    return integral_img

def get_recsum(img, X, Y, x, y, w, h):
    integral = get_integral_img(img, X, Y)
    return integral[x+w][y+h] - integral[x][y+h] - integral[x+w][y] + integral[x][y]

small_sum = get_recsum(img, X, Y, 1, 3, 2, 2)
