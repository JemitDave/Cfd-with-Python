import numpy as np,csv,os
os.chdir(r'J:\Python\Cfd_codes\Nptel_Code')
# logging.basicConfig(loggin)
m=31;n=21 #m for i,j for n
p=(m-2)*(n-2)       #p=interior points
dx=6.0/(m-1)
dy=4.0/(n-1)

psi_old=np.zeros((n,m),dtype=float)
psi_new=np.zeros((n,m),dtype=float)
As=(1.0/(dy**2.0))
Aw=(1.0/(dx**2.0))
Ap=-2.0*(   (   1.0/(dx**2.0)  )   + (  1.0/(dx**2.0)   )   )
An=(1.0/(dy**2.0))
Ae=(1.0/(dx**2.0))


#initialization and boundary conditions
psi_new[:,5:]=100.0  #bottom right
print(psi_new)

#Jacobi Iterative Method
iteration=0
error=1.0
log=open("Jacobi_error_log.txt",'w')   #for writing errors
log.write(f"Iteration:Error")

while error>1e-8:
    psi_old[:,:]=psi_new[:,:]   #replacing old psi with new values

    #iterating for interior points
    for j in range(1,n-1):
        for i in range(1,m-1):
            psi_new[j,i]=(1.0/Ap)*\
                (   -As*psi_old[j-1,i]\
                    -Aw*psi_old[j,i-1]\
                    -Ae*psi_old[j,i+1]\
                    -An*psi_old[j+1,i]\
                )

    #For Homogeneous Neumann Boundary on right wall (dpsi/dx = 0)
    psi_new[:,m-1]=psi_new[:,m-2]

    error=0.0
    for j in range(1,n-1):
        for i in range(1,m-1):
            error=error+(psi_new[j,i]-psi_old[j,i])**2.0

    error=(error/(m*n))**0.5
    print(f"""
    Iteration={iteration}\nerror={error}""")
    log.write(f"\n{iteration}\t{error}")
    iteration+=1

with open('psi_Jacobi.csv','w',newline='') as file:
    writer=csv.writer(file)
    writer.writerow(['X(I=31)','Y(J=21)','PSI'])
    for j in range(n):
        for i in range(m):
            writer.writerow([i*2,j*2,psi_new[j,i]])
