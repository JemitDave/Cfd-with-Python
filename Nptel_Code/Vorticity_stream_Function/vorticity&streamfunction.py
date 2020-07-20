import numpy as np
import pandas as pd
m=31
n=31
p=(m-2)*(n-2)       #p=interior points
dx=1.0/(m-1)
dy=1.0/(n-1)
beta=(dx/dy)
re=100.0
error_psi=0.0
error_omega=0.0
iteration=0
psi=np.zeros((m,n),dtype='float')
psi_old=np.zeros((m,n),dtype='float')
omega=np.zeros((m,n),dtype='float')
omega_old=np.zeros((m,n),dtype='float')
u=np.zeros((m,n),dtype='float')
v=np.zeros((m,n),dtype='float')

#initialization and boundary conditions
for j in range(0,n):
    for i in range(0,m):
        if j==(n-1):
            u[i,j]=1.0
#here the lid is moving on the right wall wrt to matrix
#final answer needs to be rotated 90 deg anti-clockwise
#print(u)
#initializing vorticity omega
for j in range(0,n):
    for i in range(0,m):
        if j==0: #bottom wall
            omega[i,j]=((2.0/pow(dy,2))*(psi[i,j]-psi[i,j+1]))
        elif j==(n-1): #top wall
            omega[i,j]=((2.0/pow(dy,2)*(omega[i,j]-omega[i,j-1]-u[i,j]*2.0/pow(dy,2))))
        elif i==0: #left wall
            omega[i, j] = ((2.0 / pow(dx, 2)) * (psi[i, j] - psi[i+1,j]))
        elif i==(m-1): #right wall
            omega[i, j] = ((2.0 / pow(dx, 2)) * (psi[i, j] - psi[i-1,j]))



#gs method
while True:
    for j in range(0, n):
        for i in range(0, m):
            psi_old[i,j]=psi[i,j]
            omega_old[i,j] =omega[i, j]

    #solving stream function for interior points
    for j in range(1, n-1):
        for i in range(1, m-1):
            psi[i,j]=((0.5/(1.0+pow(beta,2)))*(psi[i+1,j]+psi[i-1,j]+(pow(beta,2)*(psi[i,j+1]+psi[i,j-1]))+pow(dx,2)*omega[i,j]))

    #solving vorticity for interior points
    for j in range(1, n-1):
        for i in range(1, m-1):
            omega[i,j]=(0.5/(1.0+pow(beta,2)))*(((1.0-(psi[i,j+1]-psi[i,j-1])*(beta*re/4.0))*omega[i+1,j])+((1.0+(psi[i, j + 1] - psi[i, j - 1]) * (beta * re / 4.0)) * omega[i - 1, j])+((1.0+(psi[i+1,j] - psi[i-1, j]) * ( re / 4.0*beta)) * omega[i, j+1]*pow(beta,2))+((1.0 - (psi[i + 1, j] - psi[i - 1, j]) * (re / 4.0*beta)) * omega[i, j - 1]*pow(beta,2)))


    #updating vorticity at boundaries
    for j in range(0, n):
        for i in range(0, m):
            if j == 0:  # bottom wall
                omega[i, j] = ((2.0 / pow(dy, 2)) * (psi[i, j] - psi[i, j + 1]))
            elif j == (n - 1):  # top wall
                omega[i, j] = ((2.0 / pow(dy, 2) * (omega[i, j] - omega[i, j - 1] - u[i, j] * 2.0 / pow(dy, 2))))
            elif i == 0:  # left wall
                omega[i, j] = ((2.0 / pow(dx, 2)) * (psi[i, j] - psi[i + 1, j]))
            elif i == (m - 1):  # right wall
                omega[i, j] = ((2.0 / pow(dx, 2)) * (psi[i, j] - psi[i - 1, j]))


    #error calculation
    error_psi=0.0
    error_omega=0.0
    for j in range(1, n-1):
        for i in range(1, m-1):
            error_psi=error_psi+pow((psi[i,j]-psi_old[i,j]),2.0)
            error_omega = error_omega + pow((omega[i, j] - omega_old[i, j]), 2.0)

    error_psi_1=math.sqrt((error_psi/p))
    error_omega_1= math.sqrt((error_omega / p))
    iteration=iteration+1

    if error_omega_1< 1.0e-8 or error_psi_1<1.0e-8:
        break
print (error_psi_1)
print(error_omega_1)
#updating velocities u and v
for j in range(1, n-1):
    for i in range(1, m-1):
        u[i,j]=(0.5/dy)*(psi[i,j+1]-psi[i,j-1])
        v[i, j] = (-0.5 / dx) * (psi[i+1, j] - psi[i-1, j])


#wb=Workbook()                  #assigning workbook
#ws=wb.active                   #activating/selecting default worksheet

## convert your array into a dataframe
df = pd.DataFrame(psi)
## save to xlsx file
filepath = 'psi5.xlsx'
df.to_excel(filepath, index=True)
