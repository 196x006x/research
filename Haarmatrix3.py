from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix
import math
#getpixel((x,y)) y = height x = width

before = Image.open("lena1024.bmp")

width,height = before.size

#n段Haar変換を行う( count+1 = 段数)
count = 4

#出力画像について名前をつける
name = "trypress1024to256.bmp"
#1で出力
output = 341

#ここでは正方の画像のみを扱うこととし、一辺の長さをNとおきN*Nの画像を扱う
N = int(math.sqrt(height))
#print(N)

before_pixels = []
#print(before.getpixel((1,1)))

for y in range(height):
    matrix = []
    for x in range(width):
        if(height == 1024):
            matrix.append([before.getpixel((x,y))[0]])
        else:
            matrix.append([before.getpixel((x,y))])
    before_pixels.append(matrix)

#変換前の画像を行列計算用の変数に変換
before_matrix = np.array(before_pixels)
#print(before_matrix)
"""
for i in range(height):
    for j in range(width):
        if before_matrix[i][j] != 0:
            print(before_matrix[i][j])"""

haar = np.zeros((N*N,N*N))

#Haar変換を行列にしたものを生成
for i in range(int((N*N)/4)):
    j = (int)(i/(N/2))
    m = i % (N/2)
    ta = (int)(j*2*N+2*m)

    #print(i,j,m,ta)

    for j in (0,1,2,3):
        haar[4*i+j,ta] = 1
        haar[4*i+j,ta+1] = 1*((-1)**j)
        if(j ==  2 or j ==3):
            haar[4*i+j,ta+N] = -1
        else:
            haar[4*i+j,ta+N] = 1
        if(j == 1 or j == 2):
            haar[4*i+j,ta+N+1] = -1
        else:
            haar[4*i+j,ta+N+1] = 1

#生成完了

#print(haar)


#各成分の移動を行列で表現
transport = np.zeros((N*N,N*N))
for a in (0,1):
    for i in range(int(N/2)):
        for j in (0,1):
            for k in range(int(N/2)):
                #print(a,i,j,k)
                x = k + (i*N) + j*(int(N/2)) + a*(N*(int(N/2)))
                y = k * 4  + j + 2*a + i*N*2
                #print(x,y)
                transport[x,y] = 1

#print(transport)

#transportとhaarの積が実際の変換行列となる
change_matrix = np.dot(transport,haar/4)
#print(change_matrix)
#count(段数)乗する
change0 = change_matrix
for i in range(count):
    """
    #グラフの出力部分↓
    a = change_matrix[greenharvest]
    for i in range(N*N):
        if a[i] != 0:
            print(i,a[i])
    sum =[a[i] for i in range(N*N)]

    #print(sum)
    #pyplot.plot(range(N*N),sum,"ko")
    #pyplot.show()
    #グラフの出力部分↑"""
    change_matrix = np.dot(change_matrix,change0)


"""
#グラフの出力部分↓
a = change_matrix[greenharvest]
for i in range(N*N):
    if a[i] != 0:
        print(i,a[i])
sum =[a[i] for i in range(N*N)]

#print(sum)
pyplot.plot(range(N*N),sum,"ko")
pyplot.show()
#グラフの出力部分↑
"""
print(change_matrix[0])

count_graf = []
#change_matrixの調査
for i in range(50):
    count = 0
    for j in range((N*N-1)):
        if change_matrix[i][j] * change_matrix[i][j+1] < 0:
            count = count+1
            #print(change_matrix[i][j])
    #print(i,count)
    count_graf.append(count)

pyplot.plot(range(50),count_graf)
pyplot.show()

"""
#print(before_matrix)
    
#各行ごとに変換行列をかける
after_pixels = []
for i in range(N*N):
    matrix = np.dot(change_matrix,before_matrix[i])
    #print(matrix)
    after_pixels.append(matrix)

#print(matrix)"""

"""#print(after_pixels[100])
for i in range(width):
    print(after_pixels[800][i])"""
    

"""
#グラフの出力部分
sum = [after_pixels[i][j] for i in range(N*N) for j in range(N*N)]
print(sum)
pyplot.plot(range(N*N*N*N),sum,"ko")
pyplot.show()"""
"""
#逆変換を行う
inv_matrix = np.linalg.inv(change_matrix)
#print(inv_matrix)
after_inv = []
for i in range(N*N):
    matrix = np.dot(inv_matrix,after_pixels[i])
    after_inv.append(matrix)

#print(after_inv)
#画像の出力部分
img2 = Image.new("L",(width,height))
for y in range(height):
    for x in range(width):
        img2.putpixel((x,y),int(after_inv[y][x]))

img2.show()
if(output == 1):
    img2.save(name)"""

