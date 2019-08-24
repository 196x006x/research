from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix
import math

#count+1 = 段数
count = 1

#N*N = size
N = 4

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
print(change_matrix*16)
