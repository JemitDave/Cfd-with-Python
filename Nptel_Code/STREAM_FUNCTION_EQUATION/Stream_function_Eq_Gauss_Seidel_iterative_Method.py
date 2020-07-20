# import os
# os.chdir(r'J:\Python\Cfd_codes\Nptel_Code')
# data=open('error_log.txt').readlines()
# for line in data:
#     print(line.strip())

# The difference between the Gauss–Seidel and Jacobi methods
# is that the Jacobi method uses the values obtained from the previous
# step while the Gauss–Seidel method always applies the latest updated
# values during the iterative procedures
import numpy as np,csv,os
os.chdir(r'J:\Python\Cfd_codes\Nptel_Code\STREAM_FUNCTION_EQUATION')
# logging.basicConfig(loggin)
m=31;n=21 #m for i,j for n
p=(m-2)*(n-2)       #p=interior points
dx=6.0/(m-1)
dy=4.0/(n-1)

psi=np.zeros((n,m),dtype=float)
As=(1.0/(dy**2.0))
Aw=(1.0/(dx**2.0))
Ap=-2.0*(   (   1.0/(dx**2.0)  )   + (  1.0/(dy**2.0)   )   )
An=(1.0/(dy**2.0))
Ae=(1.0/(dx**2.0))


#initialization and boundary conditions
psi[:,5:]=100.0  #bottom right
# print(psi)

#Gauss Seidel Iterative Method
iteration=0
error=1.0
log=open("GS_error_log.txt",'w')   #for writing errors
log.write(f"Iteration:Error")

while error>1e-8:
    error=0.0

    #iterating for interior points
    for j in range(1,n-1):
        for i in range(1,m-1):
            temp=psi[j,i]
            psi[j,i]=(1.0/Ap)*\
                (   -As*psi[j-1,i]\
                    -Aw*psi[j,i-1]\
                    -Ae*psi[j,i+1]\
                    -An*psi[j+1,i]\
                )
            error=error+(psi[j,i]-temp)**2.0 # for each iteration,latest available values are used

    #For Homogeneous Neumann Boundary on right wall (dpsi/dx = 0)
    psi[:,m-1]=psi[:,m-2]

    error=(error/(m*n))**0.5
    print(f"""
    Iteration={iteration}\nerror={error}""")
    # log.write(f"error for Gauss Seidel Iterative Method")
    log.write(f"\n{iteration}\t{error}")
    iteration+=1

with open('psi_gsim.csv','w',newline='') as file:
    writer=csv.writer(file)
    writer.writerow(['X(I=31)','Y(J=21)','PSI'])
    for j in range(n):
        for i in range(m):
            writer.writerow([i*2,j*2,psi[j,i]])
