
import numpy as np,time,os,pandas as pd,csv
os.chdir("J:\\Python\\Cfd_codes\\Governing Equations\\3d_ht")
m=n=o=31
nps=m*n*o  #number of points
L=30.0
dx=L/(m-1)
dy=L/(n-1)
dz=L/(o-1)
d2x=pow(dx,2.0)
d2y=pow(dy,2.0)
d2z=pow(dz,2.0)
gxyz=(d2x*d2y+d2y*d2z+d2z*d2x)
tem_old=np.zeros((o,n,m),dtype=float)
tem_new=np.zeros((o,n,m),dtype=float)
error=1.0
iteration=0
log=open("logger.txt",'w')
# k,j,i+1=[1:-1,1:-1,2:]
# k,j,i-1=[1:-1,1:-1,0:-2]
# k,j+1,i=[1:-1,2:,1:-1]
# k,j-1,i=[1:-1,0:-2,1:-1]
# k+1,j,i=[2:,1:-1,1:-1]
# k-1,j,i=[0:-2,1:-1,1:-1]


#bcs
#on left wall ie at x=0 T=500K
tem_new[:,:,0]=500.0
#on right wall ie at x=l T=1000K
tem_new[:,:,-1]=1000.0

print(tem_new)
#jacobi method
while True:
    tem_old[:,:,:]=tem_new[:,:,:]
# iterating interior points
    tem_new[1:-1,1:-1,1:-1]=(1/(2*gxyz))*\
                            (   (tem_old[1:-1,1:-1,2:]+tem_old[1:-1,1:-1,0:-2])*d2y*d2z+\
                                (tem_old[1:-1,2:,1:-1]+tem_old[1:-1,0:-2,1:-1])*d2x*d2z+\
                                (tem_old[2:,1:-1,1:-1]+tem_old[0:-2,1:-1,1:-1])*d2x*d2y\
                            )
#neumann bc:
#on top wall
    tem_new[:,0,:]=tem_new[:,1,:]
#bottom wall
    tem_new[:,-1,:]=tem_new[:,-2,:]
#on front wall
    tem_new[0,:,:]=tem_new[1,:,:]
#back wall
    tem_new[-1,:,:]=tem_new[-2,:,:]


    error=0.0
    for k in range(0, o):
        for j in range(0, n):
            for i in range(0, m):
                error = error + pow((tem_new[k,j, i] - tem_old[k,j, i]), 2.0)#print(error)

    error = pow((error / nps),0.5)
    iteration = iteration + 1
    if iteration%100==0:
        err=round(error,5)
        print(iteration,err
        log.write(f"iteration={iteration},\t\t\terror={err}\n")
    if error < 1e-3 :break
    elif iteration>10000: break
print(f"stopped at iteration {iteration} with error {round(error,5)}")
log.close()
# print(tem_new)
value=[]
x=[]
y=[]
z=[]
for k in range(0,o):
    for j in range(0,n):
        for i in range(0,m):
            x.append(i)
            y.append(j)
            z.append(k)
            value.append(tem_new[k,j,i])

rows=zip(x,y,z,value)
with open("temperature_values.csv",'w') as f:
    writer=csv.writer(f)
    for row in rows:
        writer.writerow(row)
