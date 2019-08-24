from PIL import Image
import numpy as np
import time,sys

#press(圧縮する量)
press = 60
name = "had196.bmp"

before = Image.open("lena256ttt.bmp") #画像ファイルを開く
#print(before)

width,height = before.size#画像ファイルのサイズを測定

before_pixels = []#各ポイントの色の値をリストに代入
#print(before.getpixel((1,5)))

before_value = []
for y in range(height):
    matrix = []
    for x in range(width):
        #print(before.getpixel((x,y)))
        matrix.append([before.getpixel((x,y))])
        before_value.append([before.getpixel((x,y))])
    before_pixels.append(matrix)

befpre_value = np.array(before_value)
before_matrix = np.array(before_pixels) #リストを行列に変換
#print(before_matrix[0])

#変換前の平均、標準偏差を計算
before_mean = np.average(before_value)
before_std = np.std(before_value)
#print(before_mean,before_std)

hadmard = [[1,1],[1,-1]]

#4096*4096の行列を作成するためには12回の繰り返しが必要
for i in range(1,8):
    matrix = []
    for k in range(2 ** i):
        matrix.append([hadmard[k][j] for c in range(2) for j in range(2 ** i)])
        #二重の内包の場合後ろに書いたforが先に回る
    for k in range(2 ** i):
        matrix.append([hadmard[k][j] * (-1) ** c for c in range(2) for j in range(2 ** i)])
    #print(matrix)
    hadmard = matrix

count_graf = []
#change_matrixの調査
for i in range(height):
    count = 0
    for j in range((width-1)):
        if hadmard[i][j] * hadmard[i][j+1] < 0:
            count = count+1
            #print(change_matrix[i][j])
    #print(i,count)
    count_graf.append(count)
    
#print(count_graf)
    
for i in range(height):
    for j in range(0,(height-1)-i):
        if(count_graf[j] > count_graf[j+1]):
            count_graf[j],count_graf[j+1] = count_graf[j+1],count_graf[j]
            hadmard[j],hadmard[j+1] = hadmard[j+1],hadmard[j]


#print(count_graf)
            
#print(hadmard[1])
            
#print(hadmard)

#press分の補充行列を作成,追加
O = [0 for i in range(width)]
O = np.array(O)

press_hadmard = []
for i in range(height-press):
    press_hadmard.append(hadmard[i])

press_hadmard = np.array(press_hadmard)
hadmard = np.array(hadmard)
#startTime = time.time()
after_pixels = []
for i in range(height):
    matrix = np.dot(press_hadmard,before_matrix[i])
    after_pixels.append(matrix)
    
#after_pixels = hadmard * before_pixels
after_inv = []
for i in range(height):
    matrix = np.dot(press_hadmard.T/(height),after_pixels[i])
    after_inv.append(matrix)
    
#elaspsed = time.time() - startTime
#print(elaspsed)
#print(after_pixels)
#after_pixels = after_pixels.getA()
after_value = []
img2 = Image.new("L",(width,height))
for y in range(height):
    for x in range(width):
        value = int(after_inv[y][x])
        #print(after_pixels[x][y],int(after_pixels[x][y]))
        #print(type(0+after_pixels[x][y]))
        img2.putpixel((x,y),value)
        after_value.append(value)
        #print(after_pixels[y][x])

#逆変換後の平均、標準偏差を計算
after_value = np.array(after_value)
after_mean = np.mean(after_value)
after_std = np.std(after_value)
#print(after_mean,after_std)

Std = 0
for i in range(height*width):
    a = (before_value[i] - before_mean)
    b = (after_value[i] - after_mean)

    Std += a*b

Std = Std/(height*width)

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
img2.save(name)
   


