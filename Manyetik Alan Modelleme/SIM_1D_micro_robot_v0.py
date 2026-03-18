# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 16:34:38 2025

@author: pc64x
"""
from class_bobin import *
from class_objects import*
from class_controller import*




# Tanımlamalar ve Ölçüler 
# Bobin özellikleri 
a=100.0/1000.0; # bobin yarıçapı (m) 
N=100.0 # Bobin sargı sayısı  
I=1.0 # Akım (A)

bobin=bobin(a,i=I,z0=a/5,n=N)

# %%  Robot Ayarları ve Tanımlama 

m0=0.4 # mıknatısın manyetik dipol (A*m2)
M=0.0001 # Ağırlık (kg) 
g=1*9.81 
b= 0.001 # sürtünme kuvveti 
z0=0.0;
dz0=0.0;
robot=micro_robot_1D(M,m0) 
robo_color=(250,0,0)   
robot.set_color(robo_color)
robot.set_size(0.75/1000)
# %%


# Simulasyon ayarları 

def get_force(X):
    d_z=1e-3
    z0=X[0,0]
    z0a=X[0,0]-d_z
    z0b=X[0,0]+d_z
    B=bobin.get_magnetic_field_rotated(0.0,0.0,z0)
    B_a=bobin.get_magnetic_field_rotated(0.0,0.0,z0a)
    B_b=bobin.get_magnetic_field_rotated(0.0,0.0,z0b)
    dBz_dz=(B_b[2]-B_a[2])/(2*d_z)
    force=m0*dBz_dz
    torqe=0
    #print(B_a)
    return B,force,torqe

def dF(t,X,F):
    # T=m x B
    # F=m . (Nabla B) 
    df=np.zeros_like(X)
    B,Fz,Tx=get_force(X)
    df[0]=X[1]
    df[1]=Fz/M-g-b*X[1]/M
    return df


# %%


t0=0; ts=1; dt=0.001

n=int((ts-t0)/dt)
t=0
X=np.array([[z0],[dz0]]) #[z,dz]

SIM=simulator(t0,ts,dt,X,sim_type='RK4')
SIM.set_fcn(dF)




# %% KONTROLCÜ AYARLARI 
PID_controller=PID_controller_1D(dt,y_ref=a/10) # ♠kontrolcüyü tanımla 
PID_controller.set_parameters(kp=700) # PID parametrelerini düzenle 



# %%  SIMULASYON EKRANI VE AYARLARI  
ekran=pygame_screan_2D(min_X=[-0.1/2,-0.1/2],max_X=[0.1/2,0.1/2]) # Ekranı oluştur 
bg_color=(220,220,220) 
ekran.set_backgraun_color(bg_color) # Arka plan rengini ayarla 
ekran.set_textSize(30) # Yazı fontu büyüklüğünü ayarla 
ekran.add_robot(robot) # Bir robot geometrisi ekle 
ekran.add_coil(bobin)  # Bir bobin ekle 
# %%

running=True
say=0
t0=timer.time()
while running:
    control_current=PID_controller.apply(SIM.X[0,0]) # Kontrolcüden uygulanacak akımı hesaplat 
    control_current=4;
    # print(control_current)
    bobin.set_current(control_current)
    SIM.apply() # Simulasyonu çalıştır 
    
    x=[0.0,0.0,SIM.X[0,0]]
    v=[0.0,0.0,SIM.X[1,0]]
    
    robot.update_position(x,v)
    if SIM.adim % 1==0:    
        magnetic_field,force,torque=get_force(SIM.X) # Manyetik alanları hesapla 
        running=ekran.draw(n=SIM.adim,t=SIM.get_time(),B=magnetic_field,F=force,T=torque) # Ekranı güncelle 
        #print(SIM.adim,SIM.get_time())
    timer.sleep(dt)
    
    if SIM.adim==n: 
        running=False
t1=timer.time()    
fark=t1-t0 
print('geçen süre ',fark)
ekran.exit_simulation() # Simulasyon ekranından çık 


# %% SONUÇ GRAFİKLERİ 


plt.plot(SIM.log_T[:,0],SIM.log_X[:,0])

# plot_list_points_with_length(1,111,[(Data[:,0],Data[:,1],'-r',2),
#                                     (SIM2.log_T[:,0],SIM2.log_X[:,0],':k',1),
#                                     (SIM3.log_T[:,0],SIM3.log_X[:,0],'--g',1)],legend=['RK4','Eu','RK4a'],title='Başlık')
