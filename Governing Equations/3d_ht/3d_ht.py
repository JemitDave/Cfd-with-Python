import numpy as np,time,os,pandas as pd
m=n=o=3
L=1
dx=L/(m-1)
dy=L/(n-1)
dz=L/(o-1)
# # print(dx,dy,dz)
d2x=pow(dx,2.0)
d2y=pow(dy,2.0)
d2z=pow(dz,2.0)
gxyz=(d2x*d2y+d2y*d2z+d2z*d2x)
tem_old=np.zeros((o,n,m),dtype=float)
tem_new=np.zeros((o,n,m),dtype=float)
tem_old=tem_new
tem_new[1:-1,1:-1,1:-1]=5#interior points
# print(tem_new)
# k,j,i+1=[1:-1,1:-1,2:]
# k,j,i-1=[1:-1,1:-1,0:-2]
# k,j+1,i=[1:-1,2:,1:-1]
# k,j-1,i=[1:-1,0:-2,1:-1]
# k+1,j,i=[2:,1:-1,1:-1]
# k-1,j,i=[0:-2,1:-1,1:-1]

#interior points
tem_new[1:-1,1:-1,1:-1]=(1/2*gxyz)*\
                            (   (tem_old[1:-1,1:-1,2:]+tem_old[1:-1,1:-1,0:-2])*d2y*d2z+\
                                (tem_old[1:-1,2:,1:-1]+tem_old[1:-1,0:-2,1:-1])*d2x*d2z+\
                                (tem_old[2:,1:-1,1:-1]+tem_old[0:-2,1:-1,1:-1])*d2x*d2y\
                            )
print(tem_new)
