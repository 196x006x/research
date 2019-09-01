from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix
import math

#N*Nの画像を対象とする変換を行う。
N = 64
#Nの2乗
NN = N*N

#変換行列をリストとして作成
changeMatrix = []

#最初の１行を作成
changeMatrix.append(np.random.rand(NN)*255)

for i in range(NN):
    #NN行のシフト行列を連結によって作成する
    changeMatrix.append(np.hstack((changeMatrix[i-1][N:NN],np.random.rand(N)*255)))

#各要素に対して1と-1へ変換する
for i in range(NN):
    for node in range(NN):
        if changeMatrix[i][node] > 127:
            changeMatrix[i][node] = 1
        else:
            changeMatrix[i][node] = -1

#パターン画像を作成
pattern = Image.new("L",(1920,1080))
for index in range(NN):
    for count in [1,-1]:
        for i in range(N):
            for j in range(N):
                value = changeMatrix[index][i*N+j]
                if value == count:
                    imageValue = 255
                else:
                    imageValue = 0
                for h in range(16):
                    for w in range(16):
                        pattern.putpixel((488+(j*16)+w,28+i*16+h),imageValue)

        #パターンを画像として出力
        #pattern.show()
        if count == 1:
            name = "pattern/" + "shiftPattern" + str(N) + "plus"+ str(index) +".bmp"
        else:
            name = "pattern/" + "shiftPattern" + str(N) + "minus" + str(index) + ".bmp"
        pattern.save(name)
        
