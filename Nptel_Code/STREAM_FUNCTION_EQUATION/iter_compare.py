import numpy as np,os
os.chdir(r'J:\Python\Cfd_codes\Nptel_Code\STREAM_FUNCTION_EQUATION')
iter=[];error=[]
with open('Jacobi_error_log.txt') as data:
    val=data.readlines()
    for line in val:
        ans=line.strip().split()
        try:
            iter.append(ans[0])
            error.append(ans[1])
        except Exception as e:
            print(e)
            pass
iter.pop(0)
iter.pop(-1)
error.pop(-1)
# print(iter[-1])
# print(error[-1])
from matplotlib import pyplot as plt
# x=np.linspace(0,len(iter),1000)
# y=np.linspace(0,len(error),1000)

fig=plt.figure()
axes=fig.add_axes([0.1,0.1,0.8,0.8])
# axes.plot(x, y, 'r')
axes.plot(iter,error, 'r')
axes.set_yscale('log')
# axes.set_xscale('log')
axes.set_xlabel('x')
axes.set_ylabel('y')
axes.set_title('Error vs Iteration')
plt.show()
