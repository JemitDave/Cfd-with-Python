import numpy as np,os
from matplotlib import pyplot as plt
os.chdir(r'J:\Python\Cfd_codes\Nptel_Code\Vorticity_stream_Function')
data=np.load('vs_data.npz')
u=data['u']
v=data['v']
psi=data['psi']
omega=data['omega']
# print(u.shape)
x = np.linspace(0, 1, 301)
y = np.linspace(0, 1, 301)
X, Y = np.meshgrid(x, y)
# print(len(x))
# print(u)

fig=plt.figure(figsize=(11,7),dpi=100)
plt.contourf(X, Y,((u)**2+(v)**2)**0.5, cmap=plt.cm.hsv)
plt.colorbar()
plt.quiver(X[::10, ::10], Y[::10, ::10], u[::10, ::10], v[::10, ::10])
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
