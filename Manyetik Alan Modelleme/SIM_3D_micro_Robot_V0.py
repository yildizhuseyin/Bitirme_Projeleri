# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 12:55:18 2026

@author: pc64x
"""

from class_bobin import *
from class_objects import*
from class_controller import*





"""
robot=micro_robot_1D(M,m0) 
robo_color=(250,0,0)   
robot.set_color(robo_color)
robot.set_size(0.75/1000)
x=[0.0,0.0,z0]
v=[0.0,0.0,dz0]
robot.update_position(x,v)
q=[q0,0.0,0]
w=[dq0,0.0,0]
robot.update_rotation(q,w)
"""
# %%


    
def get_magnetic_fields(x,y,z):
    B=np.zeros([4,])
    for bobin in ekran.coils: 
        b=bobin.get_magnetic_field_rotated(x,y,z)
        B=B+b
    B[3]=np.sqrt(B[0]**2+B[1]**2+B[2]**2)
    return B
        
# Simulasyon ayarları 
def get_force(X):
    m=robot.get_magnet_vector()
    d_z=1e-3
    z0=X[0,0]
    z0a=X[0,0]-d_z
    z0b=X[0,0]+d_z
    B=get_magnetic_fields(0.0,0.0,z0)
    B_a=get_magnetic_fields(0.0,0.0,z0a)
    B_b=get_magnetic_fields(0.0,0.0,z0b)
    dBz_dz=(B_b[2]-B_a[2])/(2*d_z)
    force=m0*dBz_dz
    torqe=np.cross(m, B[:3])
    #print(B_a)
    return B,force,torqe[0]

def dF(t,X,F):
    # T=m x B
    # F=m . (Nabla B) 
    df=np.zeros_like(X)
    B,Fz,Tx=get_force(X)
    df[0]=X[1]
    df[1]=Fz/M-g-b*X[1]/M
    return df


# Tanımlamalar ve Ölçüler 
# Bobin özellikleri 
a=50.0/1000.0; # bobin yarıçapı (m) 
N=500.0 # Bobin sargı sayısı  
I=3.0 # Akım (A)

# %%  Robot Ayarları ve Tanımlama 

m0=0.124 # mıknatısın manyetik dipol (A*m2)
M=0.001 # Ağırlık (kg) 
g=0*9.81 
b= 0.05 # sürtünme kuvveti 
z0=0.0;
dz0=0.0;
q0=0.0*np.pi/180;
dq0=0.0*np.pi/180;

# %%
ekran=screan_3D(min_X=[-50,-50,-50],max_X=[50,50,50]) # Ekranı oluştur 

# robot=micro_robot_3D(ekran,M,m0) 
robot=micro_robot_3D(ekran,M,m0,Type='cylinder',D=[0,0,1],color='yellow' ) # color=(250,250,0), color='blue' 
# X: konum vektörü, V: hız vektörü
# Q: dönme açıları vektörü, W: Açısal hız vektörü 
# D: Doğrultu vektörü, Dönme işlemini daha tam anlayamadım. Şimdilik bu şekilde yönü belirlenebiliyor.   

# robo_color=(250,0,0)   
# robot.set_color(robo_color)
# robot.set_size(0.75/1000)
# x=[0.0,0.0,z0]
# v=[0.0,0.0,dz0]
# robot.update_position(x,v)
# q=[q0,0.0,0]
# w=[dq0,0.0,0]
# robot.update_rotation(q,w)
# %%



bobin1=silindirik_bobin_3D(ekran,a/2,i=I,z0=a/1,n=N)
bobin2=silindirik_bobin_3D(ekran,a/2,i=-I,z0=-a/1,n=N,Type='2D')
#bobin1=silindirik_bobin_3D(ekran,a/2,i=-I,z0=a/2,n=N,Type='3D',par=[a/4,3*a/4,a/5]) # par=[r_min,r_max,h]
#bobin2=silindirik_bobin_3D(ekran,a/2,i=-I,z0=-a/2,n=N,Type='3D',par=[a/4,3*a/4,a/5])

# ekran.add_coil(bobin1)
# ekran.add_coil(bobin2)
# %%


t0=0; ts=1; dt=0.003

n=int((ts-t0)/dt)
t=0
X=np.array([[z0],[dz0]]) #[z,dz]

SIM=simulator(t0,ts,dt,X,sim_type='RK4')
SIM.set_fcn(dF)







# %% KONTROLCÜ AYARLARI 
PID_controller=PID_controller_1D(dt,y_ref=-0.2*1000*3*a/4) # ♠kontrolcüyü tanımla 
PID_controller.set_parameters(kp=500) # PID parametrelerini düzenle 
kc=25; tc=(0.555-0.515)*1
PID_controller.set_ZNC(kc,tc,Type='PID') # PID parametrelerini düzenle 
PID_controller.set_scale_factor([1.0,1.0,0.01])



    
running=True
say=0
t0=timer.time()
data=[]


while running:
    say=say+1
    data.append([SIM.adim,SIM.get_time(),PID_controller.y_ref*1000,SIM.X[0,0]*1000])
    I_1=-1.12
    I_2=+2.8
    
    bobin1.set_current(I_1)
    bobin2.set_current(I_2)
    
    SIM.apply() # Simulasyonu çalıştır 
    
    x=[0.0,0.0,SIM.X[0,0]]
    v=[0.0,0.0,SIM.X[1,0]]

    robot.update_position(x,v)
    
    if SIM.adim % 10==0:  
        magnetic_field,force,torque=get_force(SIM.X) # Manyetik alanları hesapla 
        ekran.update(SIM.adim,SIM.t,par=[magnetic_field,force,torque,0])
    else:
        ekran.update(SIM.adim,SIM.t)
    
    # timer.sleep(0.01)
    # print(say,np.round(x,4))
    
    if SIM.adim==n: 
        running=False
t1=timer.time()    
fark=t1-t0 
print('geçen süre ',fark)



Data=np.array(data)
# %% SONUÇ GRAFİKLERİ 
    
    
plt.plot(Data[:say,0],Data[:say,2])
plt.plot(Data[:say,0],Data[:say,3])



