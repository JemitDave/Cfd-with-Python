from matplotlib import pyplot as plt
import os,csv,numpy as np
os.chdir(r'J:\Python\Cfd_codes\Nptel_Code\STREAM_FUNCTION_EQUATION')
data=open('psi_Jacobi.csv')
reader=csv.reader(data)
x=[];y=[];psi=[]
for row in reader:
    x.append(row[0])
    y.append(row[1])
    psi.append(row[2])
# psi = np.genfromtxt(data, delimiter=',')
psi=np.array(psi[1:])
X=np.array(x[1:])
Y=np.array(y[1:])
new_psi=psi.reshape(21,31)
X_1=X.reshape(21,31)
Y_1=Y.reshape(21,31)
# XA,YA=np.meshgrid(X_1,Y_1)
# fig = plt.figure(figsize=(11, 7), dpi=100)
# surf2 = plt.contour(XA,YA,new_psi, cmap='twilight_shifted')
# plt.title("Stream_Function")
# plt.colorbar(surf)
# plt.xlabel('X')
# plt.ylabel("Y")

fig, ax = plt.subplots()
fig=plt.contour(new_psi, cmap=plt.cm.RdBu)
plt.show()
