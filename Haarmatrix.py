from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix

before = Image.open("lena64.bmp")

width,height = before.size

#4段Haar変換を行う
count = 1

#ここでは正方の画像のみを扱うこととし、一辺の長さをNとおきN*Nの画像を扱う
N = height

before_pixels = []

for x in range(height):
    matrix = []
    for y in range(width):
        before_pixels.append([before.getpixel((x,y))])

#変換前の画像を行列計算用の変数に変換
before_matrix = np.matrix(before_pixels)

haar = lil_matrix((N*N,N*N))

#Haar変換を行列にしたものを生成
for i in range(int((N*N)/4)):
    j = (int)(i/(N/2))
    m = i % (N/2)
    ta = j*2*N+2*m

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
transport = lil_matrix((N*N,N*N))
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

#csr_matirixに変換　計算効率が向上するらしい
haar = haar.tocsr()
transport = transport.tocsr()
#transportとhaarの積が実際の変換行列となる
change_matrix = haar/4
#change_matrix = (transport * haar)/4
#print(change_matrix)
#count(段数)乗する
#change_matrix = change_matrix**count
#行列計算、本来は1/4のところを１にしているため計算後1/4する
after_matrix = change_matrix.dot(before_matrix)
#する必要はないが、arrayのほうが好きなのでarrayに変換
after_pixels = after_matrix.getA()
print(after_pixels)

#画像の出力
img2 = Image.new("L",(width,height))
for x in range(height):
    for y in range(width):
        img2.putpixel((x,y),int(after_pixels[(x*width)+y]))
                

img2.show()
img2.save("simout.bmp")
"""
#逆変換を行う

inv_matrix = change_matrix.I
after_inv = inv_matrix.dot(after_matrix)


#する必要はないが、arrayのほうが好きなのでarrayに変換
after_pixels = after_inv.getA()

#画像の出力
img3 = Image.new("L",(width,height))
for x in range(height):
    for y in range(width):
        img3.putpixel((x,y),int(after_pixels[(x*width)+y]))
                

img3.show()
"""
