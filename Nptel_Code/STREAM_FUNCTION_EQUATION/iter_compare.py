from matplotlib import pyplot as plt
import numpy as np,os
os.chdir(r'J:\Python\Cfd_codes\Nptel_Code\STREAM_FUNCTION_EQUATION')
iter=[];error=[]
with open('Jacobi_error_log.txt') as data:
    text=data.readlines()
with open('GS_error_log.txt') as data:
    text1=data.readlines()

for i in range(1,len(text)):
    iter.append(float(text[i].split()[0]))
    error.append(float(text[i].split()[1]))

iter1=[];error1=[]
for i in range(1,len(text1)):
    iter1.append(float(text1[i].split()[0]))
    error1.append(float(text1[i].split()[1]))

fig,ax=plt.subplots()
ax.loglog(iter,error,label='Jacobi')
ax.loglog(iter1,error1,label='Gauss Seidel')
ax.set_xlabel('log(Iterations)')
ax.set_ylabel('log(Error)')
ax.legend(loc='upper right')
ax.set_yticks([1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1e0,5,10])
plt.savefig('JacobivsGauss_Seidel(iterations_and_error).png')
plt.show()
