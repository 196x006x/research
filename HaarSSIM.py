from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix
import math
#getpixel((x,y)) y = height x = width

before = Image.open("lena256ttt.bmp")

width,height = before.size

#n段Haar変換を行う( count+1 = 段数)
count = 3

#分割割合を定める(S = 2のときは開始行を0として奇数行を落とすことになる)
S = 8

#周波数の上限を決める(周波数の上限 = 残る行の個数)
press_freq = 156
#Npress = 残す行の数(失敗)
#Npress = 1024

#出力画像について名前をつける
name = "256_156.bmp"
#1で出力
output = 1

#ここでは正方の画像のみを扱うこととし、一辺の長さをNとおきN*Nの画像を扱う
N = int(math.sqrt(height))
#print(N)

#print(before.getpixel((1,1)))

before_pixels = []
before_value = []
for y in range(height):
    matrix = []
    for x in range(width):
        if(height == 1024):
            matrix.append([before.getpixel((x,y))[0]])
            before_value.append([before.getpixel((x,y))[0]])
        else:
            matrix.append([before.getpixel((x,y))])
            before_value.append([before.getpixel((x,y))])
    before_pixels.append(matrix)

before_value = np.array(before_value)

#変換前の平均、標準偏差を計算
before_mean = np.average(before_value)
before_std = np.std(before_value)
print(before_mean,before_std)

#変換前の画像を行列計算用の変数に変換
before_matrix = np.array(before_pixels)
#print(before_matrix)

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
change_matrix = np.dot(transport,haar)
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
#print(change_matrix[2])
    
#print(before_matrix)

count_graf = []
#change_matrixの調査
for i in range(N*N):
    count = 0
    for j in range((N*N-1)):
        if change_matrix[i][j] * change_matrix[i][j+1] < 0:
            count = count+1
            #print(change_matrix[i][j])
    #print(i,count)
    count_graf.append(count)

"""
#符号の入れ替わり回数を昇順で入れ替え(失敗)
for i in range(height):
    for j in range(0,(height-1)-i):
        if(count_graf[j] > count_graf[j+1]):
            count_graf[j],count_graf[j+1] = count_graf[j+1],count_graf[j]
            change_matrix[j],change_matrix[j+1] = change_matrix[j+1],change_matrix[j]
"""

#press分の補充行列を作成,追加
O = [0 for i in range(width)]
O = np.array(O)
#print(O)

"""
#Sごとにpress
change_press = []
M = int(height/S)
for i in range(M):
    change_press.append(change_matrix[i*S])
    for j in range((S-1)):
        change_press.append(O)"""

#高周波の箇所をpress
change_press = []
press_count = 0
for i in range(N*N):
    if count_graf[i] < press_freq:
        change_press.append(change_matrix[i])
    else:
        press_count = press_count+1
        change_press.append(O)
        

"""
#並び替え後を下からpress(失敗)
change_press = []
for i in range(Npress):
    change_press.append(change_matrix[i])

for i in range(height - Npress):
    change_press.append(O)"""

#print(height - press_count)#残っている行数を表示
    
#print(change_press[1])
change_press = np.array(change_press)
#各行ごとに変換行列をかける
after_pixels = []
for i in range(N*N):
    matrix = np.dot(change_press/(height),before_matrix[i])
    #print(matrix)
    after_pixels.append(matrix)

#print(matrix)

#print(after_pixels[100])
"""for i in range(width):
    print(after_pixels[800][i])"""
    

"""
#グラフの出力部分
sum = [after_pixels[i][j] for i in range(N*N) for j in range(N*N)]
print(sum)
pyplot.plot(range(N*N*N*N),sum,"ko")
pyplot.show()"""

#逆変換を行う(必要なかった)
#inv_matrix = np.linalg.inv(change_matrix)
#print(inv_matrix)
after_inv = []
for i in range(N*N):
    matrix = np.dot(change_matrix,after_pixels[i])
    after_inv.append(matrix)

#print(after_inv)
after_value = []
#画像の出力部分
img2 = Image.new("L",(width,height))
for y in range(height):
    for x in range(width):
        value = int(after_inv[y][x])
        img2.putpixel((x,y),value)
        after_value.append(value)

#逆変換後の平均、標準偏差を計算
after_value = np.array(after_value)
after_mean = np.mean(after_value)
after_std = np.std(after_value)
print(after_mean,after_std)

#共分散を計算
Std = 0
for i in range(height*width):
    a = (before_value[i] - before_mean)
    b = (after_value[i] - after_mean)

    Std += a*b

#height*widthはそれぞれのデータの総数。合計総数ではない。
Std = Std/(height*width)

print(Std)

#破棄
after_value = []
before_value = []


#SSIMを計算する
cca = (0.01*255) * (0.01*255)
ccb = (0.03*255) * (0.03*255)

a = (2*before_mean*after_mean + cca) * (2*Std + ccb)

b = (before_mean*before_mean + after_mean*after_mean + cca) * (before_std*before_std + after_std*after_std + ccb)

SSIM = a/b

print(SSIM)

img2.show()
if(output == 1):
    img2.save(name)
