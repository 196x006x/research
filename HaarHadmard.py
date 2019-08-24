from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix
import math

width,height = 1024,1024

#n段Haar変換を行う( count+1 = 段数)
count = 4

#このHaar変換では正方の画像のみを扱うこととし、一辺の長さをNとおきN*Nの画像を扱う
N = int(math.sqrt(height))

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

#transportとhaarの積が実際の変換行列となる
change_matrix = np.dot(transport,haar)

#段数乗する
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

print(change_matrix)

Haarcount_graf = []
#change_matrixの調査
for i in range(N*N):
    count = 0
    for j in range((N*N-1)):
        if change_matrix[i][j] * change_matrix[i][j+1] < 0:
            count = count+1
            #print(change_matrix[i][j])
    #print(i,count)
    Haarcount_graf.append(count)


print("a")

#Hadmard変換行列を生成
hadmard = [[1,1],[1,-1]]

#4096*4096の行列を作成するためには12回の繰り返しが必要
for i in range(1,10):
    matrix = []
    for k in range(2 ** i):
        matrix.append([hadmard[k][j] for c in range(2) for j in range(2 ** i)])
        #二重の内包の場合後ろに書いたforが先に回る
    for k in range(2 ** i):
        matrix.append([hadmard[k][j] * (-1) ** c for c in range(2) for j in range(2 ** i)])
    #print(matrix)
    hadmard = matrix

print("a")

Hadmardcount_graf = []
#Hadmardの調査
for i in range(height):
    count = 0
    for j in range((width-1)):
        if hadmard[i][j] * hadmard[i][j+1] < 0:
            count = count+1
            #print(change_matrix[i][j])
    #print(i,count)
    Hadmardcount_graf.append(count)
"""
for i in range(height):
    for j in range(0,(height-1)-i):
        if(Hadmardcount_graf[j] > Hadmardcount_graf[j+1]):
            Hadmardcount_graf[j],Hadmardcount_graf[j+1] = Hadmardcount_graf[j+1],Hadmardcount_graf[j]
            hadmard[j],hadmard[j+1] = hadmard[j+1],hadmard[j]
        if(Haarcount_graf[j] > Haarcount_graf[j+1]):
            Haarcount_graf[j],Haarcount_graf[j+1] = Haarcount_graf[j+1],Haarcount_graf[j]
            change_matrix[j],change_matrix[j+1] = change_matrix[j+1],change_matrix[j]"""

for i in range(height):
    for j in range(width):
        if(hadmard[i][j] != change_matrix[i][j]):
            print(i,j)
            print(hadmard[i][j],change_matrix[i][j])
            break
