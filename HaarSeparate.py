from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix

before = Image.open("lena64.bmp")

width,height = before.size

#4段Haar変換を行う( count+1 = 段数)
count = 1

#ここでは正方の画像のみを扱うこととし、一辺の長さをNとおきN*Nの画像を扱う
N = height

before_pixels = []

for x in range(height):
    matrix = []
    for y in range(width):
        matrix.append(before.getpixel((x,y)))
    before_pixels.append(matrix)

#変換前の画像を行列計算用の変数に変換
before_matrix = before_pixels
#before_matrix = np.array(before_pixels)
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
    for i in range(int(height/2)):
        for j in (0,1):
            for k in range(int(width/2)):
                #print(a,i,j,k)
                x = k + (i*height) + j*(int(height/2)) + a*(height*(int(width/2)))
                y = k * 4  + j + 2*a + i*width*2
                #print(x,y)
                transport[x,y] = 1

#print(transport)

#transportとhaarの積が実際の変換行列となる
#1/4する
change_matrix = np.dot(transport,haar/4)
#print(change_matrix)

#count(段数)乗する
change0 = change_matrix
for i in range(count):
    change_matrix = np.dot(change_matrix,change0)

#print(change_matrix)
#行分割に対して適応させる
#各行に対して64*64の行列を生成する
#生成後、各対応部分について計算を行う
#生成後保持せずに計算することで空間計算量を軽減
after_pixels = []
for i in range(N*N):
    matrix = []
    calc = 0
    for k in range(N):
        matrix.append([change_matrix[i][j+(N * k)] for j in range(N)])
    for a in range(N):
        for b in range(N):
            #print(a,b,matrix[a][b],before_matrix[a][b])
            calc += matrix[a][b] * before_matrix[a][b]
    after_pixels.append(calc)

#print(after_pixels)
                

#画像の出力
img2 = Image.new("L",(width,height))
for x in range(height):
    for y in range(width):
        img2.putpixel((x,y),int(after_pixels[(x*width)+y]))
        #print(after_pixels[(x*width)+y])
                

img2.show()
#img2.save("matrixHaar.bmp")


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
img3.save("invMatrixHaar.bmp")

