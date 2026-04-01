# -*- coding: utf-8 -*-
"""
Tek bobinle 1D micro robot hareketi, simulasyonu ve kontrolü  
Aynı yönlü manyetik alan oluşturarak 
@author: pc64x
"""
from class_bobin import *
from class_objects import*
from class_controller import*




# Tanımlamalar ve Ölçüler 
# Bobin özellikleri 
a=50.0/1000.0; # bobin yarıçapı (m) 
N=500.0 # Bobin sargı sayısı  
I=3.0 # Akım (A)

bobin1=bobin(a/2,i=I,z0=a,n=N)
bobin2=bobin(a/2,i=-I,z0=-a,n=N)

# %%  Robot Ayarları ve Tanımlama 

m0=0.124 # mıknatısın manyetik dipol (A*m2)
M=0.001 # Ağırlık (kg) 
g=0*9.81 
b= 0.1 # sürtünme kuvveti 
z0=0.0;
dz0=0.0;
q0=0.0*np.pi/180;
dq0=0.0*np.pi/180;

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


# %%  SIMULASYON EKRANI VE AYARLARI  
ekran=pygame_screan_2D(min_X=[-0.2/3,-0.2/3],max_X=[0.2/3,0.2/3]) # Ekranı oluştur 
bg_color=(220,220,220) 
ekran.set_backgraun_color(bg_color) # Arka plan rengini ayarla 
ekran.set_textSize(30) # Yazı fontu büyüklüğünü ayarla 
ekran.add_robot(robot) # Bir robot geometrisi ekle 
ekran.add_coil(bobin1)  # Bir bobin ekle 
ekran.add_coil(bobin2)  # Bir bobin ekle 
# %%

running=True
say=0
t0=timer.time()
data=[]
while running:
    say=say+1
    
    if SIM.adim % 3==0:   
        kk=(0.225+2.55*abs(PID_controller.y_ref-SIM.X[0,0])/0.01)**2
        y_ref=(2*a/3)*np.sin(2*np.pi*SIM.t)
        #PID_controller.set_referance(y_ref)
        fark=PID_controller.apply(SIM.X[0,0]*1000) # Kontrolcüden uygulanacak akımı hesaplat 
        
        # fark=PID_controller.apply_with_ref(SIM.X[0,0],yref)
        control_current=0*255/3;
        I_1=1*(+control_current+fark*1.0)
        I_2=1*(-control_current-fark*1.0)
        I_1=(np.round(I_1,0)/255)*3
        I_2=(np.round(I_2,0)/255)*3
        print(fark,I_1,I_2)
        if I_1>3: 
            I_1=3
        elif I_1<-3: 
            I_1=-3
        if I_2>3: 
            I_2=3
        elif I_2<-3: 
            I_2=-3
        
    # print(control_current)
    bobin1.set_current(I_1)
    bobin2.set_current(I_2)
    SIM.apply() # Simulasyonu çalıştır 
    
    x=[0.0,0.0,SIM.X[0,0]]
    v=[0.0,0.0,SIM.X[1,0]]
    
    robot.update_position(x,v)
    ref_point=[0.0,0,PID_controller.y_ref]
    data.append([SIM.adim,SIM.get_time(),PID_controller.y_ref,SIM.X[0,0]*1000,I_1,I_2])
    if SIM.adim % 1==0:    
        magnetic_field,force,torque=get_force(SIM.X) # Manyetik alanları hesapla 
        running=ekran.draw(n=SIM.adim,t=SIM.get_time(),
                           B=magnetic_field,F=force,
                           T=torque,P=ref_point) # Ekranı güncelle 
        #print(SIM.adim,SIM.get_time())
    # timer.sleep(dt)
    
    if SIM.adim==n: 
        running=False
t1=timer.time()    
fark=t1-t0 
print('geçen süre ',fark)
ekran.exit_simulation() # Simulasyon ekranından çık 

Data=np.array(data)
# %% SONUÇ GRAFİKLERİ 

plt.figure(1)
plt.plot(Data[:say,0],Data[:say,2])
plt.plot(Data[:say,0],Data[:say,3])

plt.figure(2)
plt.plot(Data[:say,0],Data[:say,4])
plt.plot(Data[:say,0],Data[:say,5])

# plot_list_points_with_length(1,111,[(Data[:,0],Data[:,1],'-r',2),
#                                     (SIM2.log_T[:,0],SIM2.log_X[:,0],':k',1),
#                                     (SIM3.log_T[:,0],SIM3.log_X[:,0],'--g',1)],legend=['RK4','Eu','RK4a'],title='Başlık')
