from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix

before = Image.open("lena512.bmp")

width,height = before.size

#n段Haar変換を行う(count = 段数)
count = 2

#N*Nの正方の画像を扱う
N = width

#print((int(N/2)))

before_pixels = []

for x in range(height):
    matrix = []
    for y in range(width):
        #print(before.getpixel((x,y)))
        before_pixels.append(before.getpixel((x,y)))

#print(before_pixels)とすると謎のバグを起こす
#変換前の画像を行列計算用の変数に変換
before_matrix = np.array(before_pixels)
#print(before_matrix)

haarA = np.zeros((N,N))
haarB = np.zeros((N,N))
haarC = np.zeros((N,N))
OOO = np.zeros((N,N))

#要素となる行列を作成
for j in [0,1]:
    for i in range((int(N/2))):
        if j == 0:
            haarA[i,i*2] = 1
            haarA[i,i*2+1] = 1
            
            haarC[i,i*2] = -1
            haarC[i,i*2+1] = -1
        else:
            haarA[(int(N/2))+i,i*2] = 1
            haarA[(int(N/2))+i,i*2+1] = -1

            haarC[(int(N/2))+i,i*2] = -1
            haarC[(int(N/2))+i,i*2+1] = 1


#分解した行列を作成
"""
失敗作？
x_matrix = []
for i in range(N):
    matrix = []
    for j in range(N):
        if i < (int(N/2)):
            if j == i*2 or j == i*2+1:
                matrix.append(haarA)
            else:
                matrix.append(OOO)
        else:
            if j == (i - (int(N/2)))*2:
                matrix.append(haarA)
            elif j == (i - (int(N/2)))+1:
                matrix.append(haarC)
            else:
                matrix.append(OOO)
    x_matrix.append(matrix)
"""


x_matrix = []
for k in [0,1]:
    for i in range((int(N/2))):
        matrix = []
        for j in range(N):
            if k == 0:
                if j == i*2 or j == i*2+1:
                    #print("aa")
                    matrix.append(haarA)
                else:
                    #print("o")
                    matrix.append(OOO)
            if k == 1:
                if j == i*2:
                    #print("aaa")
                    matrix.append(haarA)
                elif j == i*2+1:
                    #print("ccc")
                    matrix.append(haarC)
                else:
                    #print("oo")
                    matrix.append(OOO)
        #print("ooo")
        x_matrix.append(matrix)

#print(x_matrix)


haar_matrix = []
for i in range(N):
    print(i)
    matrix = []
    for j in range(N):
        calc = 0
        for k in range(N):
            if x_matrix[i][k] is OOO or x_matrix[k][j] is OOO:
                konomi = 0
            else:
                #print(i,k,j)
                #print(x_matrix[i][k],x_matrix[k][j])
                #print(np.dot(x_matrix[i][k],x_matrix[k][j]))
                calc += np.dot(x_matrix[i][k],x_matrix[k][j])
        matrix.append(calc)
    haar_matrix.append(matrix)
#print(haar_matrix)


after_pixels = []
for i in range(N):
    print(i)
    for j in range(N):
        calc = 0
        for k in range(N):
            for m in range(N):
                #試験的に1段階のx_matrixで書く
                if haar_matrix[i][k][j,m] != 0:
                    #print(i,j,k,m)
                    calc += before_matrix[m+k*N] * (haar_matrix[i][k][j,m]/16)
        after_pixels.append(calc)

#画像の出力部分
img2 = Image.new("L",(width,height))
for x in range(height):
    for y in range(width):
        img2.putpixel((x,y),int(after_pixels[(x*width)+y]))

img2.show()
img2.save("Haar512.bmp")

        

