#lid driven cavity problem

import os,csv,numpy as np
from matplotlib import pyplot as plt, cm
import logging
os.chdir(r'J:\Python\Cfd_codes\Nptel_Code\Vorticity_stream_Function')
# logging.basicConfig(level=logging.DEBUG,filename='vs.log',filemode='w')
# logging.disable(level=logging.DEBUG)
m=301
n=301
p=(m-2)*(n-2)       #p=interior points
dx=1.0/(m-1)
dy=1.0/(n-1)
# beta=(dx/dy)
beta=1.0
re=100.0 #reynolds number rho*v*l/mu
error_psi=0.0
error_omega=0.0
iteration=0
psi=np.zeros((m,n),dtype='float')
psi_old=np.zeros((m,n),dtype='float')
omega=np.zeros((m,n),dtype='float')
omega_old=np.zeros((m,n),dtype='float')
u=np.zeros((m,n),dtype='float')
v=np.zeros((m,n),dtype='float')
# logging.debug(f"""
# u={u}\n\nv={v}\n\npsi={psi}\n\nomega={omega}
# """)
#initialization and boundary conditions

#velocity on the top wall (matrix bottom)
u[n-1,:]=1.0
#logging.debug(f"u after ic and bc=\n{u}")
data=open('error.txt','w')
#Bc for psi
"""
We impose normal velocity at each boundary and find bc for psi
u=dpsi/dy;  v=-dpsi/dx
    left wall=>u=0; dpsi/dy=0; ie psi=constant,
    similar for all walls,psi is constant
constant stream function is a streamline and 2 stream lines never meet.
along all 4 boundaries, psi is same i.e. psi=0
pg(215)
"""

#initializing vorticity omega
"""
Vorticity is 2*angular velocity of curl of velocity
w=-[ d2psi/dx2  +   d2psi/dy2   ]
    left wall,right wall   =>u=0; dpsi/dy=0;  d2psi/dy2=0;    Therefore w=-[ d2psi/dx2 ]
    bottom wall            =>v=0; dpsi/dx=0;  d2psi/dx2=0;    Therefore w=-[ d2psi/dy2 ]
pg(217)
"""
for j in range(0,n):
    for i in range(0,m):
        if (j==0): #bottom wall
            omega[j,i]= (2.0/(dy**2.0)) * (psi[j,i]-psi[j+1,i])
        elif (j==(n-1)): #top wall
            omega[j,i]= (2.0/(dy**2.0))  * (psi[j,i]-psi[j-1,i] - (dy * u[j,i] ))
            # omega[j,i]= (2.0/pow(dy,2))  *(   (psi[j,i]-psi[j-1,i]) - ( (1.0/dy) * u[j,i] ) )
        elif (i==0): #left wall
            omega[j,i] = (2.0 / (dx**2.0))  *  (psi[j,i] - psi[j,i+1])
        elif (i==(m-1)): #right wall
            omega[j,i] = (2.0 / (dx**2.0))  *  (psi[j,i] - psi[j,i-1])
        else:omega[j,i]=0.0
#logging.debug(f"omega after ic and bc=\n{psi[n-1,1]},{psi[n-2,1]},{dy},{u[n-1,1]}\n{omega}")


#gs method
# print('solving using gs')
while True:
    print('in loop')
    print(f"iter={iteration},\terr_psi={error_psi},\terror_omega={error_omega}")
    #logging.debug(f"it={iteration}")
    for j in range(0, n):
        for i in range(0, m):
            psi_old[j,i]=psi[j,i]
            omega_old[j,i] =omega[j,i]

    #solving stream function for interior points
    for j in range(1, n-1):
        for i in range(1, m-1):
            psi[j,i]=   ( 0.5/ (1.0+(beta**2.0) ) )*\
            (\
                 (    psi[j,i+1]+psi[j,i-1]                     )\
                +(    (beta**2.0)  *  (psi[j+1,i]+psi[j-1,i])   )\
                +(    (dx**2.0)    *  omega[j,i]                )\
            )
    #logging.debug(f"solved_psi=\n{psi}")
    #solving vorticity for interior points
    for j in range(1, n-1):
        for i in range(1, m-1):
            omega[j,i]=   ( 0.5/ (1.0+(beta**2.0) )  ) * \
            (\
             (    (1.0-(  (psi[j+1,i] - psi[j-1,i]) * ((beta*re) /4.0)  )   ) *omega[j,i+1]                )\
            +(    (1.0+(  (psi[j+1,i] - psi[j-1,i]) * ((beta * re) / 4.0)  )) * omega[j,i - 1]             )\
            +(    (1.0+(  (psi[j,i+1] - psi[j,i-1]) * ( re / (4.0*beta)  ) )) *(beta**2.0)*  omega[j+1,i]    )\
            +(    (1.0-(  (psi[j,i+1] - psi[j,i-1]) * ( re / (4.0*beta) )  )) *(beta**2.0) *omega[j-1,i]     )\
            )
    #logging.debug(f"solved_omega=\n{omega}")


    #updating vorticity at boundaries

    for j in range(0,n):
        for i in range(0,m):
            if (j==0): #bottom wall
                omega[j,i]= (2.0/(dy**2.0)) * (psi[j,i]-psi[j+1,i])
            elif (j==(n-1)): #top wall
                omega[j,i]= (2.0/(dy**2.0))  * (psi[j,i]-psi[j-1,i] - (dy * u[j,i] ))
                # omega[j,i]= (2.0/pow(dy,2))  *(   (psi[j,i]-psi[j-1,i]) - ( (1.0/dy) * u[j,i] ) )
            elif (i==0): #left wall
                omega[j,i] = (2.0 / (dx**2.0))  *  (psi[j,i] - psi[j,i+1])
            elif (i==(m-1)): #right wall
                omega[j,i] = (2.0 / (dx**2.0))  *  (psi[j,i] - psi[j,i-1])

    #logging.debug(f"updated vorticity omega=\n{psi[n-1,1]},{psi[n-2,1]},{dy},{u[n-1,1]}\n{omega}")
    #error calculation
    error_psi=0.0
    error_omega=0.0
    for j in range(1, n):
        for i in range(1, m):
            error_psi=    error_psi   + (    (psi[j,i]-psi_old[j,i])      **2.0   )
            error_omega = error_omega + (    (omega[j,i] - omega_old[j,i])** 2.0  )

    error_psi=(error_psi/((m-1)*(n-1)))**0.5
    # error_omega=(error_omega / p)**0.5
    error_omega=(error_omega/((m-1)*(n-1)))**0.5
    print(f"err_psi={error_psi},err_ome={error_omega}")
    #logging.debug(f"END OF LOOP\nIteration={iteration}\nerror_psi={error_psi}\terror_omega={error_omega}")
    data.write(f"{iteration},{error_psi},{error_omega}")
    if (error_psi<1e-6 and error_omega<1e-3):break
    iteration=iteration+1
    if iteration%100==0:
        np.savez("vs_data.npz",u=u,v=v,psi=psi,omega=omega)

print('out of loop')
 #updating velocities u and v
for j in range(1, n-1):
    for i in range(1, m-1):
        # u=dpsi/dy;    v=-dpsi/dx
        u[j,i]=(0.5/dy) *   (psi[j+1,i]-psi[j-1,i])
        v[j,i] = (-0.5 / dx) * (psi[j,i+1] - psi[j,i-1])


#results
with open('vorti_stream.txt','w') as note:
    for j in range(n):
        y=j*dy
        for i in range(m):
            x=i*dx
            note.write(f"{x},{y},{u[j,i]},{v[j,i]},{psi[j,i]},{omega[j,i]}")
np.savez("vs_data.npz",u=u,v=v,psi=psi,omega=omega)
# logging.debug(f"""
# u={u}\n\nv={v}\n\npsi={psi}\n\nomega={omega}
# """)
