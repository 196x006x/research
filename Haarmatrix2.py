from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix

before = Image.open("lena64.bmp")

width,height = before.size

#n段Haar変換を行う( count+1 = 段数)
count = 0

#ここでは正方の画像のみを扱うこととし、一辺の長さをNとおきN*Nの画像を扱う
N = height

#表示する行の番号を示す
greenharvest = 0


before_pixels = []
print(before.getpixel((1,1)))

for x in range(height):
    matrix = []
    for y in range(width):
        #print(before.getpixel((x,y)))
        before_pixels.append([before.getpixel((x,y))])

#変換前の画像を行列計算用の変数に変換
before_matrix = np.array(before_pixels)
print(before_matrix)

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
    #グラフの出力部分↓
    a = change_matrix[greenharvest]
    for i in range(N*N):
        if a[i] != 0:
            print(i,a[i])
    sum =[a[i] for i in range(N*N)]

    #print(sum)
    #pyplot.plot(range(N*N),sum,"ko")
    #pyplot.show()
    #グラフの出力部分↑
    change_matrix = np.dot(change_matrix,change0)

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
#行列計算、本来は1/4のところを１にしているため計算後1/4する
after_pixels = np.dot(change_matrix,before_matrix)
#print(after_pixels)


#画像の出力
img2 = Image.new("L",(width,height))
for x in range(height):
    for y in range(width):
        img2.putpixel((x,y),int(after_pixels[(x*width)+y]))
        #print(after_pixels[(x*width)+y])
                

img2.show()
#img2.save("matrixHaar.bmp")"""
"""
#逆変換を行う

inv_matrix = np.linalg.inv(change_matrix)
#print(inv_matrix)
after_inv = np.dot(inv_matrix,after_pixels)


#(逆変換の行列が疎であるか確かめるためにグラフで出力)グラフの出力部分↓

a = inv_matrix[200]
#print(a)
sum =[a[i] for i in range(N*N)]

#print(sum)
pyplot.plot(range(N*N),sum,"ko")
pyplot.show()

#グラフの出力部分↑


#画像の出力
img3 = Image.new("L",(width,height))
for x in range(height):
    for y in range(width):
        img3.putpixel((x,y),int(after_inv[(x*width)+y]))
                

img3.show()
#img3.save("invMatrixHaar.bmp")
"""

