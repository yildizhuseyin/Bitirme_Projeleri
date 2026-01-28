# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 16:34:38 2025

@author: pc64x
"""
from class_bobin import *






# Tanımlamalar 
# Bobin özellikleri 
a=100/1000; # bobin yarıçapı (m) 
N=100 # Bobin sargı sayısı  
I=1 # Akım (A)

bobin=bobin(a,i=I,z0=a/5,n=N)

m=0.4 # mıknatısın manyetik dipol (A*m2)
M=0.0001 # Ağırlık (kg) 
g=0*9.81 
b= 0.001 # sürtünme kuvveti 
z0=0;
dz0=0;
"""
 dzz M = Fz - M g - dz b
 dzz=Fz/M-g-b dz/M
 
 x0=z 
 x1=dz 
 
 dx0=x1
 dx1=Fz/M-g-b x1/M

F=m . N B 
F=m k . (d_dy j+d_dz k) (Bx i + By j)
F=dBz/dz
"""
def get_force(X):
    d_z=1e-3
    z0=X[0,0]
    z0a=X[0,0]-d_z
    z0b=X[0,0]+d_z
    B_a=bobin.get_magnetic_field_rotated(0,0,z0a)
    B_b=bobin.get_magnetic_field_rotated(0,0,z0b)
    dBz_dz=(B_b[2]-B_a[2])/(2*d_z)
    force=m*dBz_dz
    #print(B_a)
    return force

def dF(t,X):
    # T=m x B
    # F=m . (Nabla B) 
    df=np.zeros_like(X)
    Fz=get_force(X)
    df[0]=X[1]
    df[1]=Fz/M-g-b*X[1]/M
    return df


t0=0; ts=1; dt=0.0001
n=int((ts-t0)/dt)
t=0
X=np.array([[z0],[dz0]]) #[z,dz]
Data=np.zeros([n,3])
for i in range(n):
    # e=a/10-X[0,0]
    # I=e*25
    # print(I)
    # bobin.set_current(I)
    
    # dX=dF(t,X)  # Euler yönteminde türev 
    K1=dF(t,X)
    K2=dF(t+dt/2,X+K1*dt/2)
    K3=dF(t+dt/2,X+K2*dt/2)
    K4=dF(t+dt,X+K3*dt)
    dX=(1/6)*(K1+2*K2+2*K3+K4) # Runge Kutta İçin 
    X=X+dX*dt
    Data[i,:]=[t,X[0,0],X[1,0]]
    t=t+dt
    

plt.plot(Data[:,0],Data[:,1])


