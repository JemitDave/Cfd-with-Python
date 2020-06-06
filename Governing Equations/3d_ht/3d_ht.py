import numpy as np,time,os,pandas as pd
m=n=o=3
L=1
dx=L/(m-1)
dy=L/(n-1)
dz=L/(o-1)
d2x=pow(dx,2.0)
d2y=pow(dy,2.0)
d2z=pow(dz,2.0)
gxyz=(d2x*d2y+d2y*d2z+d2z*d2x)
tem_old=np.zeros((o,n,m),dtype=float)
tem_new=np.zeros((o,n,m),dtype=float)
tem_old=tem_new
# k,j,i+1=[1:-1,1:-1,2:]
# k,j,i-1=[1:-1,1:-1,0:-2]
# k,j+1,i=[1:-1,2:,1:-1]
# k,j-1,i=[1:-1,0:-2,1:-1]
# k+1,j,i=[2:,1:-1,1:-1]
# k-1,j,i=[0:-2,1:-1,1:-1]
#
#bcs
#on left wall ie at x=0 T=500K
tem_new[:,:,0]=500
#on right wall ie at x=l T=1000K
tem_new[:,:,-1]=1000


'''

'''
#jacobi method
while True:
    tem_old[:,:,:]=tem_new[:,:,:]
# iterating interior points
    tem_new[1:-1,1:-1,1:-1]=(1/2*gxyz)*\
                            (   (tem_old[1:-1,1:-1,2:]+tem_old[1:-1,1:-1,0:-2])*d2y*d2z+\
                                (tem_old[1:-1,2:,1:-1]+tem_old[1:-1,0:-2,1:-1])*d2x*d2z+\
                                (tem_old[2:,1:-1,1:-1]+tem_old[0:-2,1:-1,1:-1])*d2x*d2y\
                            )
#neumann bc:
#on top wall
    tem_new[:,0,:]=tem_new[:,1,:]
#bottom wall
    tem_new[:,-1,:]=tem_new[:,-2,:]


    error=0.0
    for j in range(0, n):
        for i in range(0, m):
            error = error + pow((tem_new[j, i] - tem_old[j, i]), 2.0)#print(error)

    error = pow((error / (m * n)),0.5)
    iteration = iteration + 1
    print(iteration)
    if error < 1e-6   :
        break
    #elif iteration>1500: break

print(tem_new)
