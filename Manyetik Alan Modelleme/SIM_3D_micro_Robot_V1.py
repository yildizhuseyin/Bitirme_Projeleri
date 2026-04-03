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


"""   
def get_magnetic_fields(x,y,z):
    B=np.zeros([3,])
    for bobin in ekran.coils: 
        b=bobin.get_magnetic_field_rotated(x,y,z)
        B=B+b
    # B[3]=np.sqrt(B[0]**2+B[1]**2+B[2]**2)
    return B
"""     
direction_vector=np.array([0,0,1])
# Simulasyon ayarları 
def get_force(X):
    # mm=np.array([0,0,m0]) #robot.get_magnet_vector()
    # print(robot.sphare*180/np.pi)
    m=robot.get_magnet_vector()
    XX=robot.X/1000#X0#X[0,:]
#    B,dB_dX=ekran.get_magnetic_gradient(X[0,0],X[0,1],X[0,2])
    B,dB_dX=ekran.get_magnetic_gradient(XX[0],XX[1],XX[2])
    T=np.cross(m, B)
    F=np.dot(m,dB_dX)
    T_sphare=convert_vector_cartesian_to_spherical(T, robot.sphare[1], robot.sphare[2])
    #print(B_a)
    return B,F,T

def dF(t,X,F):
    # T=m x B
    # F=m . (Nabla B) 
    df=np.zeros_like(X)
    B,F,T=get_force(X)
    df[0,:]=X[1,:]
    df[1,:]=F[:]/M-g[:]-b[:]*X[1,:]/M
    df[2,:]=X[3,:]
    df[3,:]=(T[:]-bq[:]*X[3,:])/J
    return df



tt0=0; tts=2.25; dt=0.0025

# Tanımlamalar ve Ölçüler 
# Bobin özellikleri 
a=50.0/1000.0; # bobin yarıçapı (m) 
N=500.0 # Bobin sargı sayısı  
I=3.0 # Akım (A)

# %%  Robot Ayarları ve Tanımlama 

m0=0.124 # mıknatısın manyetik dipol (A*m2)
M=0.001 # Ağırlık (kg) 
J=1e-8 # Robot atalet momenti 
g=np.array([0.0,0.0,0*9.81]) # Yer çekimi vektörü 
b=[0.1,0.1,0.1] # doğrusal sürtünme katsayısı
bq=[1e-5,1e-5,1e-5] # açısal sürtünme katsayısı 
X0=[0/1000,0/1000,-15/1000]; # Robot başlangıç konumları x,y,z 
dX0=[0.0,0.0,0.0]; # Robot başlangıç hızları Vx,Vy,Vz 
Q0=[40*np.pi/180,0*np.pi/180,0*np.pi/180];# Robot başlangıç açıları alfa_x,alfa_y,alfa_z 
dQ0=[0.0,0.0,0.0];# Robot başlangıç açısal hızları w_x,w_y,w_z 


# %%
ekran=screan_3D(min_X=[-50,-50,-50],max_X=[50,50,50]) # Ekranı oluştur 

# robot=micro_robot_3D(ekran,M,m0) 
robot=micro_robot_3D(ekran,M,m0,Type='cylinder',X=X0,D=[0,0,+1],color='yellow' ) # color=(250,250,0), color='blue' 
# X: konum vektörü, V: hız vektörü
# Q: dönme açıları vektörü, W: Açısal hız vektörü 
# D: Doğrultu vektörü, Dönme işlemini daha tam anlayamadım. Şimdilik bu şekilde yönü belirlenebiliyor.   


bobin1=cylindirical_coil_3D(ekran,a/2,i=+1*I,z0=1*a/1,n=N,alfa=[-0,0,0])
bobin2=cylindirical_coil_3D(ekran,a/2,i=0.5*I,z0=-a/1,n=N,Type='2D')
# bobin1=cylindirical_coil_3D(ekran,a/2,i=-I,z0=a/2,n=N,Type='3D',par=[a/4,3*a/4,a/5]) # par=[r_min,r_max,h]
# bobin2=cylindirical_coil_3D(ekran,a/2,i=-I,z0=-a/2,n=N,Type='3D',par=[a/4,3*a/4,a/5])
"""
cizgi_bobin1=infinite_line_coil_3D(ekran,i=-1*1e3,y0=-a/2,n=1,L=100,alfa=[-0,0,0])
cizgi_bobin2=infinite_line_coil_3D(ekran,i=-0*1e3,y0=a/2,n=1,L=100,alfa=[0,0,0])
cizgi_bobin3=infinite_line_coil_3D(ekran,i=-0*1e3,y0=a/2,n=1,L=100,alfa=[0,0,90])
cizgi_bobin4=infinite_line_coil_3D(ekran,i=-1*1e3,y0=a/2,n=1,L=100,alfa=[0,0,-90])
"""
# ekran.add_coil(bobin1)
# ekran.add_coil(bobin2)
# %%



N=10
#ekran.plot_magnetic_field_vectors([-00,00,1],[-50,50,N],[-40,40,N],scale=100.0)
#ekran.plot_magnetic_field_vectors([-50,50,N],[-0,0,1],[-40,40,N],scale=100.0)
# ekran.plot_magnetic_field_vectors([-40,40,N],[-40,40,N],[-0,0,1],scale=100.0)
# ekran.plot_magnetic_field_vectors([-40,40,N],[-40,40,N],[-40,40,N],scale=100.0)

# ekran.plotter.update()

# timer.sleep(2)


## Simulasyon yarat 
#tt0=0; tts=0.5; dt=0.003

n=int((tts-tt0)/dt)
t=0
X_ref=np.array([X0,dX0,Q0,dQ0]) #[z,dz]
SIM=simulator(tt0,tts,dt,X_ref,isAdd=True,sim_type='RK4')
SIM.set_fcn(dF)
# Hareket kısıtlama için kullandığımız matris. 1 olduğunda aktif oluyor, 0 olduğunda pasif. 
Matrix=[[1,1,1],
   [1,1,1],
   [1,0,0],
   [1,0,0]]
SIM.set_add_matrix(Matrix)



# %% KONTROLCÜ AYARLARI 
yref=25
PID_controller=PID_controller_1D(dt,y_ref=yref) # ♠kontrolcüyü tanımla 
PID_controller.set_parameters(kp=500) # PID parametrelerini düzenle 
kc=25; tc=(0.555-0.515)*1
PID_controller.set_ZNC(kc,tc,Type='PID') # PID parametrelerini düzenle 
PID_controller.set_scale_factor([1.0,1.0,1.00])


x=SIM.X[0,:]; #[0.0,0.0,SIM.X[0,2]]
v=SIM.X[1,:]; #[0.0,0.0,SIM.X[1,2]]
q=SIM.X[2,:];
w=SIM.X[3,:];
robot.update_position(x,v)
robot.update_rotation(q, w)
    
running=True
say=0
t0=timer.time()
data=[]

Q_e=SIM.X[2,:]
while running:
    say=say+1
    if SIM.adim % 2==0:   
        yref=-0#*np.sin(2*np.pi*SIM.t)
        #PID_controller.set_referance(y_ref)
        i_c=PID_controller.apply_with_ref(SIM.X[0,2]*1000,yref) # Kontrolcüden uygulanacak akımı hesaplat 
        i_1=+1*250+i_c
        i_2=+1*250-i_c
        I_1=i_1*(3/255)
        I_2=i_2*(3/255)
        
        bobin1.set_current(I_1)
        bobin2.set_current(I_2)
        
        #cizgi_bobin1.set_current(1e3*np.sin(np.pi*2*SIM.t))    
        #cizgi_bobin4.set_current(1e3*np.cos(np.pi*2*SIM.t))  
    data.append([SIM.adim,SIM.get_time(),yref,SIM.X[0,2]*1000])
    
    
      
    
    if -40/1000<SIM.X[0,0] and 40/1000>SIM.X[0,0] and-40/1000<SIM.X[0,1] and 40/1000>SIM.X[0,1] and -40/1000<SIM.X[0,2] and 40/1000>SIM.X[0,2]:
        SIM.apply() # Simulasyonu çalıştır 
        x=SIM.X[0,:]; #[0.0,0.0,SIM.X[0,2]]
        v=SIM.X[1,:]; #[0.0,0.0,SIM.X[1,2]]
        q=SIM.X[2,:];
        w=SIM.X[3,:];
        robot.update_position(x,v)
        robot.update_rotation(q, w)
        # p=robot.geo_robot.position[:]
        # robot.geo_robot.position = [0, 0, 0]
        DQ=q-Q_e
        
        direction_vector=aply_rotation_and_translation(direction_vector, DQ*180/np.pi)

        if SIM.adim % 20==0:  
            #ekran.delate_arrows()
            #ekran.plot_magnetic_field_vectors([-00,00,1],[-30,30,5],[-30,30,10],scale=100.0)

            Position=robot.geo_robot.position
            magnetic_field,force,torque=get_force(robot.X/1000) # Manyetik alanları hesapla
            ref_point=np.array([0,0,yref])
            ekran.update(SIM.adim,SIM.t,par=[magnetic_field,force,torque,ref_point])
        else:
            ekran.update(SIM.adim,SIM.t)
    else: 
        print('Simulasyon limitleri aşıldı')
        running=False    
    # timer.sleep(0.01)
    # print(say,np.round(x,4))
    
    if SIM.adim==n: 
        running=False
        
t1=timer.time()  
# timer.sleep(dt)  
fark=t1-t0 
print('geçen süre ',fark)



Data=np.array(data)
# %% SONUÇ GRAFİKLERİ 
    
 
plot_list_points(1,111,[(Data[:say,1],Data[:say,2],'-k'),
                        (Data[:say,1],Data[:say,3],'-r')],legend=['ref','z'],title='Pozisyon (z)',figsize =(16, 14))   
 


