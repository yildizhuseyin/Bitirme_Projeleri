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

def dF(t,X,F):
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
SIM=simulator(t0,ts,dt,X,sim_type='euler')
SIM.set_fcn(dF)

SIM2=simulator(t0,ts,dt,X,sim_type='euler')
SIM2.set_fcn(dF)

SIM3=simulator(t0,ts,dt,X,sim_type='RK4')
SIM3.set_fcn(dF)

Data=np.zeros([n,3])
for i in range(n):
    SIM.apply()
    SIM2.apply()
    SIM3.apply()
    Data[i,:]=[SIM.t,SIM.X[0,0],SIM.X[1,0]]
    



# SIM2.run()


# SIM3.run()


plt.plot(SIM2.log_T[:,0],SIM2.log_X[:,0])

plot_list_points_with_length(1,111,[(Data[:,0],Data[:,1],'-r',2),
                                    (SIM2.log_T[:,0],SIM2.log_X[:,0],':k',1),
                                    (SIM3.log_T[:,0],SIM3.log_X[:,0],'--g',1)],legend=['RK4','Eu','RK4a'],title='Başlık')
