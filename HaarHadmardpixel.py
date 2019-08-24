from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix
import math
import csv

before = Image.open("lena1024.bmp")

width,height = before.size

#n段Haar変換を行う( count+1 = 段数)
count = 4

#press
press = 600

#このHaar変換では正方の画像のみを扱うこととし、一辺の長さをNとおきN*Nの画像を扱う
N = int(math.sqrt(height))

before_pixels = []
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

#print(change_matrix)

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


#print("a")

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

#print("a")

Hadmardcount_graf = []
#change_matrixの調査
for i in range(height):
    count = 0
    for j in range((width-1)):
        if hadmard[i][j] * hadmard[i][j+1] < 0:
            count = count+1
            #print(change_matrix[i][j])
    #print(i,count)
    Hadmardcount_graf.append(count)

for i in range(height):
    for j in range(0,(height-1)-i):
        if(Hadmardcount_graf[j] > Hadmardcount_graf[j+1]):
            Hadmardcount_graf[j],Hadmardcount_graf[j+1] = Hadmardcount_graf[j+1],Hadmardcount_graf[j]
            hadmard[j],hadmard[j+1] = hadmard[j+1],hadmard[j]

#press分の補充行列を作成,追加
O = [0 for i in range(width)]
O = np.array(O)

press_hadmard = []
for i in range(press):
    press_hadmard.append(hadmard[i])

for i in range(height - press):
    press_hadmard.append(O)

#高周波の箇所をpress
change_press = []
press_count = 0
for i in range(N*N):
    if Haarcount_graf[i] < press:
        change_press.append(change_matrix[i])
    else:
        press_count = press_count+1
        change_press.append(O)

with open("hadmard.csv","w") as f:
    writer = csv.writer(f,lineterminator = "\n")
    writer.writerows(press_hadmard)
    
change_press = np.array(change_press)
press_hadmard = np.array(press_hadmard)

"""with open("haar.csv","w") as f:
    writer = csv.writer(f,lineterminator = "\n")
    writer.writerow(change_press)"""


"""
after_haar = []
after_hadmard = []
for i in range(N*N):
    after_haar.append(np.dot(change_press/(height),before_matrix[i]))
    after_hadmard.append(np.dot(press_hadmard/(height),before_matrix[i]))

after_inv_haar = []
after_inv_hadmard = []
for i in range(N*N):
    after_inv_haar.append(np.dot(change_matrix,after_haar[i]))
    after_inv_hadmard.append(np.dot(hadmard,after_hadmard[i]))

print("lets judge")

for y in range(height):
    for x in range(width):
        print(after_inv_haar[y][x],after_inv_hadmard[y][x])
        if(after_inv_haar[y][x] != after_inv_hadmard[y][x]):
            print("not")"""
            
        

