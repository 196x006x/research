from PIL import Image
from matplotlib import pyplot
import numpy as np
from scipy.sparse import lil_matrix,csr_matrix

N = 512
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
print(x_matrix)

konomi = x_matrix
count = 8
for i in range(count):
    print(i)
    x_matrix = np.dot(x_matrix,konomi)
    
print(konomi)
print(x_matrix)
