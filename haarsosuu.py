from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix

before = Image.open("lena512.bmp")

width,height = before.size

#n段Haar変換を行う(count = 段数)
count = 9

cut = 4 ** 9

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

print(haarA)

"""
a = 0
b = 2
c= 3
x_matrix = []
for k in [0,1]:
    for i in range((int(N/2))):
        matrix = []
        for j in range(N):
            if k == 0:
                if j == i*2 or j == i*2+1:
                    #print("aa")
                    matrix.append(b)
                else:
                    #print("o")
                    matrix.append(a)
            if k == 1:
                if j == i*2:
                    #print("aaa")
                    matrix.append(b)
                elif j == i*2+1:
                    #print("ccc")
                    matrix.append(c)
                else:
                    #print("oo")
                    matrix.append(a)
        #print("ooo")
        x_matrix.append(matrix)

x_matrix = np.array(x_matrix)
#print(x_matrix)

konomi = 1
for i in range(count):
    #print(i)
    konomi = np.dot(konomi,x_matrix)
    
print(konomi)
#print(x_matrix)

matrix_set = []
for i in range(count+1):
    matrix = 1
    doublehit = count - i
    threehit = i
    for j in range(doublehit):
        matrix = np.dot(matrix,haarA)
    for j in range(threehit):
        matrix = np.dot(matrix,haarC)
    matrix_set.append(matrix)

haar_matrix = []

for i in range(N):
    matrix = []
    for j in range(N):
        tm = konomi[i][j]
        n = 0
        for k in range(count+1):
            if tm % 3 == 0:
                tm = tm/3
                n += 1
            else:
                break
        matrix.append(matrix_set[n])
    haar_matrix.append(matrix)

after_pixels = []
for i in range(N):
    for j in range(N):
        print(i,j)
        calc = 0
        for k in range(N):
            for m in range(N):
                #試験的に1段階のx_matrixで書く
                if haar_matrix[i][k][j,m] != 0:
                    #print(i,j,k,m)
                    calc += before_matrix[m+k*N] * (haar_matrix[i][k][j,m]/cut)
        after_pixels.append(calc)

#画像の出力部分
img2 = Image.new("L",(width,height))
for x in range(height):
    for y in range(width):
        img2.putpixel((x,y),int(after_pixels[(x*width)+y]))

img2.show()
img2.save("Haar512.bmp")
            """


    
    
