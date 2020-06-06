import matplotlib
import numpy as np
np.set_printoptions(linewidth=np.inf,precision=2)
import math
from openpyxl import workbook
import pandas as pd
from matplotlib import pyplot as plt

m=21
n=21
h=10.0
k=10.0
tinf=300.0
iteration=0
error=1.0
dx=5.0/(m-1)
dy=5.0/(n-1)
beta=dx/dy
gamma=1.0/(2.0*(1+pow(beta,2.0)))
tem_new=np.zeros((n,m),dtype='double')
tem_old=np.zeros((n,m),dtype='double')
def TDMA(x,y,tem_old):
    #q =np.zeros((m - 1), dtype='double')
    q=-4.0
    r = p =1.0
    s= np.zeros((n,m), dtype='double')
    rr = np.zeros((m), dtype='double')
    ss = np.zeros((n,m), dtype='double')
    for j in range(1,n-1):
        for i in range(1,m-1):
            if i ==1:
                #q[i] = -2.0 * (1.0 + pow((beta), 2.0))
                s[j, i]=-pow((beta),2)*(tem_old[j-1,i]+tem_old[j+1,i])-tem_new[j,i-1]
            elif i==m-2:
                s[j, i] = -pow((beta), 2) * (tem_old[j - 1, i] + tem_old[j + 1, i]) - tem_new[j,i+1]
            else:
                s[j, i] = -pow((beta), 2) * (tem_old[j - 1, i] + tem_old[j + 1, i])


    # Direct Sweep
    for i in range(1,m-1):
        if i == 1:
            try:
                rr[i] = r/ q
                ss[y,i] = s[y,i] / q
            except IndexError: continue
        else:
            try:
                rr[i] = r / (q - p* rr[i - 1])
                ss[y,i] = (s[y,i] - p* ss[y,i - 1]) / (q - p * rr[i - 1])
            except IndexError: continue

    # Inverse Sweep
    tem_new[y,m-2] = ss[y,m-2]
    for i in range(3, m):
        tem_new[y,m - i] = ss[y,m - i] - rr[m - i ] * tem_new[y,m - i +1]


#top, left , right bc
for j in range(0,n):
    for i in range(0,m):
        if i==0 or i==m-1  or j==n-1 :
            tem_new[j,i]=500.0
reversed_tem = tem_new[::-1]
print(reversed_tem)

while True:
    for j in range(0, n):
        for i in range(0, m):
            tem_old[j, i] = tem_new[j, i]
    # iterating interior point
    for y in range(1, n-1):
        for x in range(1, m-1):
            TDMA(x,y,tem_old)
    # convective boundary on bottom
    for i in range(1, m-1):
        tem_new[0, i ] = ( 4.0*tem_new[1,i]-tem_new[2,i]+(2.0*h*dy*tinf/k))/(3.0+(2.0*h*dy/k))

    error=0.0
    for j in range(0, n):
        for i in range(0, m):
            error = error + pow((tem_new[j, i] - tem_old[j, i]), 2.0)
    #print(error)

    error = pow((error / (m * n)),0.5)
    iteration = iteration + 1
    print('itr=',iteration)#,end='\r')
    if error < 1e-3:
        break
    elif iteration>3000: break

print(iteration,error)
#print(psi_new)
print('')
reversed_tem = tem_new[::-1]
print(reversed_tem)
print('maxtemp= ',tem_new.max())
print('mintemp= ',tem_new.min())


x = np.linspace(0, m,n )
y = np.linspace(0, m, n)
x_1, y_1 = np.meshgrid(x, y)
plt.contourf(x_1, y_1, tem_new, cmap='hsv')
plt.colorbar()
plt.show()

df = pd.DataFrame(reversed_tem)
filepath = '2D heat Cond with line gauss seidel and tdma.xlsx'
df.to_excel(filepath, index=True)
