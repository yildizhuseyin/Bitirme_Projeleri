# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 22:02:42 2025

@author: pc64x
"""
import numpy as np
import pygame
import random
import math 
import pyvista as pv
import time 
from scipy import special

Mu0=4*np.pi*1e-7 # Boşluğun manyetik geçirgenliği 


def get_Rotx(aci):# Derece 
    R=np.array([[1.0,0.0,0.0],
                [0.0,np.cos(aci*np.pi/180.0),-np.sin(aci*np.pi/180.0)],
                [0.0,np.sin(aci*np.pi/180.0),np.cos(aci*np.pi/180.0)]])
    return R

class micro_robot_1D:
    
    def __init__(self,M,m0,X=[0.0,0.0,0.0],V=[0.0,0.0,0.0],Q=[0.0,0.0,0.0],W=[0.0,0.0,0.0]):#pos=[x,y,z]
        self.M=M
        self.m0=m0
        self.X=np.array(X) # m
        self.V=np.array(V) # m/s 
        self.Q=np.array(Q) # Radian 
        self.W=np.array(W) # Radian / s
        self.color=(random.randrange(0, 255, 2),random.randrange(0, 255, 2),random.randrange(0, 255, 2))
        self.size=5/1000
        self.geo=None 
        self.isGeo3D=False
        
    
    def set_geo3D(self,geo):
        self.geo=geo
        self.isGeo3D=True
    
    def set_color(self,color):
        self.color=color
    def set_size(self,size):
        self.size=size
    
    def update_position(self,x,v): # m olarak güncellenecek 
        self.X=np.array(x)
        self.V=np.array(v)
    def update_rotation(self,q,w): # Radian olarak güncellenecek 
        self.Q=np.array(q)
        self.W=np.array(w)
        
    def get_magnet_vector(self):
        magnet_vector=np.zeros([3,])
        magnet_vector[1]=self.m0*np.sin(self.Q[0])
        magnet_vector[2]=self.m0*np.cos(self.Q[0])
        return magnet_vector
        
        
        
        
class pygame_screan_2D:
    # --- SABİTLER ---
    # pip install pygame 
    WIDTH, HEIGHT = 1200, 800 # Toplam Pencere Boyutu
    MAP_WIDTH = 800           # Harita Alanı Genişliği
    SIDEBAR_WIDTH = WIDTH - MAP_WIDTH
    METERS_TO_PIXELS = 80.0   # 1 Metre = 80 Piksel (10m harita için)
    
    # Renkler
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    SOFT_GRAY=(150,150,150)
    DARK_GRAY = (50, 50, 50)
    RED = (200, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 200)
    YELLOW = (255, 255, 0)
    
    def __init__(self,min_X=[-1,-1],max_X=[1,1],screan_size=[1200,800],title='simulation'):
        pygame.init()
        self.screan_size=screan_size
        self.width = screan_size[0]*0.66
        self.height = screan_size[1]
        # self.screan_size=np.array([self.width,self.height],dtype=np.int32)
        self.min_val = np.array(min_X)
        self.max_val = np.array(max_X)
        self.zero_point=[self.width/2,self.height/2]
        self.lengths=(self.max_val-self.min_val)
        self.scale=self.screan_size/self.lengths
        self.title = title
        self.robots=[]
        self.coils=[]
        self.robot_count=0
        self.coil_count=0
        self.background_color=self.GRAY
        
        # pygame settings
        self.screen = pygame.display.set_mode((self.screan_size[0], self.screan_size[1]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.surface = pygame.Surface((self.width, self.height))
        self.font = pygame.font.SysFont('Arial', 14)
        self.keys = pygame.key.get_pressed()
        self.text_size=13
        
    
        pygame.display.set_caption(title)

    def set_textSize(self,size):
        self.text_size=size
        self.font = pygame.font.SysFont('Arial', size)
        
    def exit_simulation(self):
        pygame.quit()
    
    def set_backgraun_color(self,color):
        self.background_color=color
    
    def add_robot(self,robo):
        self.robots.append(robo)
        self.robot_count=len(self.robots)
        
    def add_coil(self,coil):
        self.coils.append(coil)
        self.coil_count=len(self.coils)
    
    def draw(self,n=0,t=0,B=[],F=[],T=[],P=[]):
        running = True
        self.screen.fill(self.background_color)
        # self.screen.fill("purple")
        # Başlık
        title_surf = self.font.render(self.title, True, self.WHITE)
        self.surface.blit(title_surf, (5, 5))
        

        # koordinat Çizgileri (0V)
        # mid_y = self.height / 2
        # pygame.draw.line(self.surface, self.GRAY, (0, mid_y), (self.width, mid_y), 1)
        # mid_x = self.height / 2
        # pygame.draw.line(self.surface, self.GRAY, (mid_x,0), (mid_x,self.height ), 1)


        #self.draw_text(self.screen,"Micro Robot Simulation V.0",(10, 10),self.DARK_GRAY,pos_type='left')
        self.draw_transparent_text(self.screen,"Micro Robot Simulation V.0",(250,10),self.DARK_GRAY)
        str_n="n: "+str(n)
        str_time="t: "+str(t)
        str_B="B: "+str(np.round(B,5))
        str_F="F: "+str(np.round(F,5))
        str_T="T: "+str(np.round(T,7))
        str_RefP="P_ref: "+str(np.round(P,4)*1000)
        self.draw_transparent_text(self.screen,str_n,(850,10),self.DARK_GRAY) 
        self.draw_transparent_text(self.screen,str_time,(950,10),self.DARK_GRAY)
        self.draw_transparent_text(self.screen,str_B,(850,50),self.BLUE)
        self.draw_transparent_text(self.screen,str_F,(850,80),self.RED)
        self.draw_transparent_text(self.screen,str_T,(850,110),self.RED)
        
        if not P==[]:
            x=self.zero_point[0]+P[1]*self.scale[0] 
            y=self.zero_point[1]-P[2]*self.scale[1]
            pygame.draw.circle(self.screen, self.DARK_GRAY, (x,y), 6)
            self.draw_transparent_text(self.screen,str_RefP,(850,140),self.DARK_GRAY)
            
        self.draw_coordinates()
        self.draw_coils()
        self.draw_robots() ## Robotları çiz 
        # Veri Çizgileri
        points = []
        pygame.display.flip()

        self.clock.tick(60)  # limits FPS to 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        if self.keys[pygame.K_q]:
            running = False
            
        
        return running 
    
    
    def draw_line(self,screen,color, start_pos, length, angle_degrees=0, size=1):
        """
        Belirli bir başlangıç noktasından, uzunlukta ve açıda bir çizgi çizer.
    
        Args:
            surface (pygame.Surface): Çizimin yapılacağı yüzey (genellikle 'screen').
            color (tuple): Çizgi rengi (örneğin: (255, 0, 0)).
            start_pos (tuple): Çizginin başlangıç (x, y) koordinatları.
            length (int/float): Çizginin piksel cinsinden uzunluğu.
            angle_degrees (int/float): Yatay eksenle yapılan açı (derece cinsinden).
            width (int): Çizgi kalınlığı.
            
        Returns:
            tuple: Çizginin bitiş noktası (end_x, end_y).
        """
        angle_radians = math.radians(angle_degrees)
        end_x = start_pos[0] + length * math.cos(angle_radians)
        end_y = start_pos[1] - length * math.sin(angle_radians) # Y-ekseni ters çevrildi
        end_pos = (int(end_x), int(end_y))
        pygame.draw.line(screen, color, start_pos, end_pos, size)
        return end_pos
    
    def draw_line_with_positions(self,screen, color, start_pos, end_pos, size=2):
        pygame.draw.line(screen, color, start_pos, end_pos, size)
        
    def draw_vector(self,screen,color,start_pos,length,angle_degrees=0, size=1):
        angle_radians = math.radians(angle_degrees)
        end_x = start_pos[0] + length * math.cos(angle_radians)
        end_y = start_pos[1] - length * math.sin(angle_radians) # Y-ekseni ters çevrildi
        end_pos = (int(end_x), int(end_y))
        self.draw_line(screen,color, start_pos, length, angle_degrees=angle_degrees, size=size)
        self.draw_line(screen,color, end_pos, length/4, angle_degrees=angle_degrees+150, size=size)
        self.draw_line(screen,color, end_pos, length/4, angle_degrees=angle_degrees-150, size=size)
        return 0 
    
    def draw_transparent_text(self,surface, text, pos,color, size=None,font_name=None):
        """
        Belirli bir (x, y) koordinatına şeffaf arka planla yazı çizer.
    
        Args:
            surface (pygame.Surface): Çizimin yapılacağı yüzey (genellikle 'screen').
            text (str): Ekrana yazılacak metin.
            color (tuple): Yazı rengi (RGB formatında).
            x (int/float): Yazının sol üst köşesinin X koordinatı.
            y (int/float): Yazının sol üst köşesinin Y koordinatı.
            size (int): Font boyutu (piksel).
            font_name (str, optional): Kullanılacak font adı. None ise varsayılan font kullanılır.
        """
        if size==None: 
            size=self.text_size

        # 1. Font Nesnesi Oluşturma (Önceki Fonksiyondan Alınmıştır)
        if font_name is None:
            font = pygame.font.Font(None, size)
        else:
            try:
                font = pygame.font.SysFont(font_name, size)
            except pygame.error:
                font = pygame.font.Font(None, size)
                
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = pos
        surface.blit(text_surface, text_rect)
    
    def draw_text(self,screen,text,pos,color,size=None,font_name=None,pos_type='left'):
        if size==None: 
            size=self.text_size
        else: 
            size=20
            
        if font_name is None:
            font = pygame.font.Font(None, size)
        else:
            try:
                font = pygame.font.SysFont(font_name, size)
            except pygame.error:
                font = pygame.font.Font(None, size)
        """
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        # Display some text
        # font = pygame.font.Font(None, 36)
        # pos=(10, 10, 10)
        text = font.render(text, size,pos)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        """
        background = pygame.Surface(self.screen.get_size())
        # background = background.convert()
        # background.fill((250, 250, 250))
        # Display some text
        font = pygame.font.Font(None, 36)
        text = font.render(text, size, color)
        textpos = text.get_rect()
        if pos_type=='center':
            textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        # Blit everything to the screen
        screen.blit(background, (0,0))
        
    def draw_coordinates(self):
        start_pos_x=pygame.Vector2(self.zero_point[0]-0.66*self.width/2,self.zero_point[1])
        start_pos_y=pygame.Vector2(self.zero_point[0],self.zero_point[1]+0.66*self.height/2)
        pygame.draw.circle(self.screen, self.SOFT_GRAY, (self.zero_point[0],self.zero_point[1]), 4)
        self.draw_line( #Çizgi çiz 
            self.screen, 
            self.SOFT_GRAY, 
            (self.width,0), 
            self.height, 
            -90, 
            size=2
            )
        self.draw_line( #Çizgi çiz 
            self.screen, 
            self.SOFT_GRAY, 
            start_pos_x, 
            0.66*self.width, 
            0, 
            size=2
            )
        self.draw_line( #Çizgi çiz 
            self.screen, 
            self.SOFT_GRAY, 
            start_pos_y, 
            0.66*self.height, 
            90, 
            size=2
            )
        
    def draw_coils(self):
        say=0
        self.draw_transparent_text(self.screen,"COİLS",(850,420),self.BLUE)
        for coil in self.coils:
            say=say+1
            x=self.zero_point[0]+coil.pos[1]*self.scale[0] 
            y=self.zero_point[1]-coil.pos[2]*self.scale[1]
            line_length = 10000*coil.a
            angle=coil.alfa
            start_point=pygame.Vector2(x-0.5*line_length*math.cos(angle),y-0.5*line_length*math.sin(angle))
            coil_pos = pygame.Vector2(x,y)
            if coil.I >0: 
                color=self.RED
            elif coil.I <0: 
                color=self.BLUE
            else: 
                color=self.SOFT_GRAY
            pygame.draw.circle(self.screen, color, coil_pos,5)
            #draw_line(screen,color, start_pos, length, angle_degrees=0, size=1)
            self.draw_line( #Çizgi çiz 
                self.screen, 
                color, 
                start_point, 
                line_length, 
                angle, 
                size=2
                )
            str_I="coil_ "+str(say)+" : "+str(np.round(coil.I,4))+" A"
            
            self.draw_transparent_text(self.screen,str_I,(850,420+say*30),self.BLUE)
            
    def draw_robots(self):
        # Çizgi ayarları
        
        for robo in self.robots:
            x=self.zero_point[0]+robo.X[1]*self.scale[0] 
            y=self.zero_point[1]-robo.X[2]*self.scale[1]
            line_length = 100*robo.m0
            angle=robo.Q[0]*180/np.pi
            # start_point=pygame.Vector2(x-0.5*line_length*math.sin(angle),y+0.5*line_length*math.cos(angle))
            start_point=pygame.Vector2(x,y)
            robo_pos = pygame.Vector2(x,y)
            pygame.draw.circle(self.screen, robo.color, robo_pos, robo.size*self.scale[0])
            #self.draw_line(self.RED,robo_pos,robo.m0*10,+90,1)#☺robo.Q[0]
            
            self.draw_vector( #Çizgi çiz 
                self.screen, 
                self.GREEN, 
                start_point, 
                line_length, 
                -angle+90, 
                size=4
            )
            str_X="X: "+str(np.round(robo.X*1000,4))+" mm"
            str_V="V: "+str(np.round(robo.V*1000,4))
            str_Q="Q: "+str(np.round(robo.Q*180/np.pi,4))+" Drc"
            str_W="W: "+str(np.round(robo.W*180/np.pi,4))
            self.draw_transparent_text(self.screen,str("ROBOT"),(850,200),self.RED)

            self.draw_transparent_text(self.screen,str_X,(850,230),self.RED)
            self.draw_transparent_text(self.screen,str_V,(850,260),self.RED)
            self.draw_transparent_text(self.screen,str_Q,(850,290),self.RED)
            self.draw_transparent_text(self.screen,str_W,(850,320),self.RED)
         
            
         
            
         
            
         
            
         
            
         
            
         
            
# %%   3D GRAFİKLER PYVISTA LIBRARY
       
# 3. Transformasyon Fonksiyonu
def get_transformation_matrix(position, rotation_deg):
    """
    position: [x, y, z]
    rotation_deg: [roll, pitch, yaw] (derece cinsinden)
    """
    x, y, z = position
    rx, ry, rz = np.radians(rotation_deg)
    
    # Rotasyon Matrisleri
    Rx = np.array([[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]])
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0], [np.sin(rz), np.cos(rz), 0], [0, 0, 1]])
    
    R = Rz @ Ry @ Rx  # Toplam rotasyon
    
    # 4x4 Matris Oluşturma
    mat = np.eye(4)
    mat[:3, :3] = R
    mat[:3, 3] = [x, y, z]
    return mat
            
class screan_3D:
    
    def __init__(self,min_X=[-1,-1,-1],max_X=[1,1,1],background='white',title='3D simulation',grid_on=False):
        self.scale=1000
        self.min_val = np.array(min_X)
        self.max_val = np.array(max_X)
        print('Çalışma alanı (mm):',self.min_val,self.max_val)
        # 1. Sahne ve Plotter Ayarları
        self.plotter = pv.Plotter(title="PyVista Micro Robot Simülasyonu")
        self.background=background
        self.plotter.set_background(self.background)
        
        
        # 1x1'lik bir düzlem oluştur ve bunu 10 parçaya böl
        if grid_on:
            # plotter.show_bounds()
            self.plotter.show_grid()
            resolution=20
            grid_plane_x = pv.Plane(center=(self.min_val[0], 0, 0), direction=(1, 0, 0), 
                                  i_size=self.max_val[1]*2, j_size=self.max_val[2]*2, i_resolution=resolution, j_resolution=resolution)
            grid_plane_y = pv.Plane(center=(0, self.min_val[1], 0), direction=(0, 1, 0), 
                                  i_size=self.max_val[0]*2, j_size=self.max_val[2]*2, i_resolution=resolution, j_resolution=resolution)
            grid_plane_z = pv.Plane(center=(0, 0, self.min_val[2]), direction=(0, 0, 1), 
                                  i_size=self.max_val[0]*2, j_size=self.max_val[1]*2, i_resolution=resolution, j_resolution=resolution)
            self.plotter.add_mesh(grid_plane_x, color="grey", style="wireframe")
            self.plotter.add_mesh(grid_plane_y, color="grey", style="wireframe")
            self.plotter.add_mesh(grid_plane_z, color="grey", style="wireframe")
            
        # Oditoryum (1x1x1 sınırlarını göstermek için bir kutu)
        self.box = pv.Box(bounds=(self.min_val[0], self.max_val[0],
                             self.min_val[1], self.max_val[1], 
                             self.min_val[2], self.max_val[2]))
        self.plotter.add_mesh(self.box, color='black', style='wireframe', opacity=0.2)
        
        ray_x0 = pv.Line([0, 0, 0], [self.min_val[0], 0, 0])
        ray_x1 = pv.Line([0, 0, 0], [self.max_val[0], 0, 0])
        self.plotter.add_mesh(ray_x0,color='darkred')  # red again
        self.plotter.add_mesh(ray_x1,color='red')  # red again
        
        ray_y0 = pv.Line([0, 0, 0], [0, self.min_val[1], 0])
        ray_y1 = pv.Line([0, 0, 0], [0, self.max_val[1], 0])
        self.plotter.add_mesh(ray_y0,color='darkgreen')  # red again
        self.plotter.add_mesh(ray_y1,color='lightgreen')  # red again
        
        ray_z0 = pv.Line([0, 0, 0], [0, 0, self.min_val[2]])
        ray_z1 = pv.Line([0, 0, 0], [0, 0, self.max_val[2]])
        self.plotter.add_mesh(ray_z0,color='darkblue')  # red again
        self.plotter.add_mesh(ray_z1,color='lightblue')  # red again
        
        sphere_source = pv.Sphere(radius=1)
        # Robotun başlangıç konumu (merkezde)
        initial_pos = [0.0, 0.0, 0.0]
        robot_actor = self.plotter.add_mesh(sphere_source, color='blue', smooth_shading=True)

        
        arrow_actor =self.plotter.add_mesh(pv.Arrow(start=(0,0,0), direction=(1.0,0,0),tip_radius=0.1, shaft_radius=0.04, tip_length=0.25,scale=10), color='red')
        arrow_actor =self.plotter.add_mesh(pv.Arrow(start=(0,0,0), direction=(0.0,1,0),tip_radius=0.1, shaft_radius=0.04, tip_length=0.25, scale=10), color='green')
        arrow_actor =self.plotter.add_mesh(pv.Arrow(start=(0,0,0), direction=(0.0,0,1),tip_radius=0.1, shaft_radius=0.04, tip_length=0.25,scale=10), color='blue')
        
        self.plotter.add_camera_orientation_widget()

        self.plotter.add_axes()
        self.plotter.camera_position = [(self.max_val[0]*3.1, self.max_val[1]*2.0, 1*self.max_val[2]*2.2), (0.0, 0.0, 0.0), (0, 0, 1)] # Kamera açısı

        # İnteraktif pencereyi aç (ama bloklama, kod devam etsin)
        self.plotter.show(interactive_update=True)
        
        self.text_info=self.plotter.add_text("SIM BİLGİ", position=(10, 700), font_size=9, color='black')
        self.text_magnetic_field=self.plotter.add_text("B :", position=(10, 660), font_size=9, color='blue')
        self.text_force=self.plotter.add_text("F :", position=(10, 640), font_size=9, color='red')
        self.text_torqe=self.plotter.add_text("T :", position=(10, 620), font_size=9, color='red')
        self.text_referance_point=self.plotter.add_text("T :", position=(10, 600), font_size=9, color='red')

        self.text_robot=self.plotter.add_text("ROBOT BİLGİ", position=(10, 400), font_size=9, color='red')
        
        self.text_coils=self.plotter.add_text("BOBİN BİLGİ", position=(10, 200), font_size=9, color='darkgreen')
        
        
        self.robot=None
        self.robots=[]
        self.robot_count=0 
        
        self.coils=[]
        self.coil_count=0 

    def add_robot(self,robot):
        self.robot=robot
    
    def add_coil(self,coil):
        self.coils.append(coil)
        self.coil_count=len(self.coils)    
    
    def update(self,n,t,par=[]):
        T=np.round(t,4)
        self.text_info.input=f"SIM BİLGİ \n n:{n}   t:{T}"
        if not par==[]:
            b=np.round(par[0],6)
            f=np.round(par[1],6)
            trq=np.round(par[2],6)
            Pref=np.round(par[3]*self.scale,2)
            self.text_magnetic_field.input=f"B :{b}"
            self.text_force.input=f"F :{f}"
            self.text_torqe.input=f"T :{trq}"
            self.text_referance_point.input=f"Ref :{Pref}"    
        self.text_robot.input=f"ROBOT BİLGİ \n X:{self.robot.X} \n V:{self.robot.V}  \n Q:{self.robot.Q}  \n W:{self.robot.W}"
        str_text=f"BOBIN BILGI \n"
        say=0
        for coil in self.coils:
            say=say+1
            str_text=str_text+f"Coil {say}   I:{coil.I} A\n"    
        self.text_coils.input=str_text
        
        self.plotter.update()
    
    
    
    
    
class micro_robot_3D:
    def __init__(self,ekran,M,m0,color=None,Type='sphare',size=[5/2,6/1],X=[0.0,0.0,0.0],V=[0.0,0.0,0.0],Q=[0.0,0.0,0.0],W=[0.0,0.0,0.0],D=[0.0,0.0,1.0]):#pos=[x,y,z]
        self.M=M
        self.scale=1000
        self.m0=m0
        self.ekran=ekran
        self.Type=Type
        if not color==None:
            self.color=color
        else: 
            self.color=(random.randrange(0, 255, 2),random.randrange(0, 255, 2),random.randrange(0, 255, 2))
        self.size=size
        self.X=np.array(X) # m
        self.V=np.array(V) # m/s 
        self.Q=np.array(Q) # Radian 
        self.W=np.array(W) # Radian / s
        self.D=np.array(D) # Doğrultu vektörü 
        self.color=color#(random.randrange(0, 255, 2),random.randrange(0, 255, 2),random.randrange(0, 255, 2))
        robot_direction=(self.D[0], self.D[1], self.D[2])
        if Type=='sphare':
            sphere_source = pv.Sphere(radius=self.size[0],
                                      direction=(0.0, 0.0, 1.0))
            # Robotun başlangıç konumu (merkezde)
            #initial_pos = [0.0, 0.0, 0.0]
            self.geo = self.ekran.plotter.add_mesh(sphere_source, color=self.color, smooth_shading=True)
            self.geo.position = self.X
        elif Type=='cylinder':
            silindir=pv.Cylinder(  # noqa: PLR0917
                center= (0.0, 0.0, 0.0),
                direction=robot_direction,
                radius= self.size[0],
                height= self.size[1],
                resolution = 10,
                capping= True)
            self.geo_robot=self.ekran.plotter.add_mesh(silindir,color=self.color)  # red again
        self.geo_robot.position = self.X
        self.geo_direction =self.ekran.plotter.add_mesh(pv.Arrow(start=(0,0,0), direction=robot_direction,tip_radius=0.075, shaft_radius=0.03, tip_length=0.25,scale=12), color=self.color)
        self.geo_fields =self.ekran.plotter.add_mesh(pv.Arrow(start=(0,0,0), direction=(0,0,1),tip_radius=0.075, shaft_radius=0.03, tip_length=0.25,scale=12), color='pink')

        
        self.size=size
        self.geo=None 
        self.isGeo3D=True
        
        self.ekran.add_robot(self)
    
    
    def set_color(self,color):
        self.color=color
        self.geo_robot.color=color
        self.geo_direction.color=color
        self.geo_fields.color=color
        
    def set_size(self,size):
        self.size=size
    
    def update_position(self,x,v): # m olarak güncellenecek 
        self.X=np.round(np.array(x)*self.ekran.scale,2)
        self.V=np.round(np.array(v)*self.ekran.scale,2)
        self.geo_robot.position = self.X
        self.geo_direction.position=self.X
        
        
    def update_rotation(self,q,w): # Radian olarak güncellenecek 
        self.Q=np.round(np.array(q),2)
        self.W=np.round(np.array(w),2)
        
    def get_magnet_vector(self):
        magnet_vector=np.zeros([3,])
        magnet_vector[1]=self.m0*np.sin(self.Q[0])
        magnet_vector[2]=self.m0*np.cos(self.Q[0])
        return magnet_vector
        
  


class silindirik_bobin_3D: 
    dl=1e-4
    
    def __init__(self,ekran,a,i=1.0,n=1.0,z0=0.0, alfa=0.0,Type='2D',par=[],color=None):
        self.ekran=ekran
        self.a=a; 
        self.I=i;
        self.N=n; 
        self.z0=z0; 
        self.dl= self.a/100
        self.alfa=alfa
        
        self.start_position=(0, 0, z0)
        self.start_direction=(0, 0, 1)
        
        Rg=self.get_Rotx(-self.alfa);
        r=np.array([[0],[0],[self.z0]])
        r_=np.dot(Rg,r)
        self.pos=r_
        
        if not color==None:
            self.color=color#(random.randrange(0, 255, 2),random.randrange(0, 255, 2),random.randrange(0, 255, 2))
        else: 
            self.color=(random.randrange(100, 200, 2),random.randrange(50, 150, 2),0)
        
        if Type=='1D' :
            coil_geo = pv.Circle(radius=self.a*0.5*self.ekran.scale, 
                                 resolution=10)
            self.ekran.plotter.add_mesh(coil_geo, color="yellow", line_width=5, label="Yörünge")
        
        elif Type=='2D' or par==[]:
            if par==[]:
                par=[self.a*0.9,self.a*1.1]
            coil_geo = pv.Disc(  # noqa: PLR0917
                center = (0.0, 0.0, z0*self.ekran.scale),
                inner = par[0]*self.ekran.scale,
                outer = par[1]*self.ekran.scale,
                normal = (0.0, 0.0, 1.0),
                r_res = 1,
                c_res = 20
            )
        elif Type=='3D':
            coil_ic=pv.Cylinder(  # noqa: PLR0917
                center = (0.0, 0.0, z0*self.ekran.scale),
                direction=(0.0, 0.0, 1.0),
                radius= par[0]*self.ekran.scale,
                height= 1.1*par[2]*self.ekran.scale,
                resolution = 20,
                capping= True)

            coil_dis=pv.Cylinder(  # noqa: PLR0917
                center = (0.0, 0.0, z0*self.ekran.scale),
                direction=(0.0, 0.0, 1.0),
                radius= par[1]*self.ekran.scale,
                height= par[2]*self.ekran.scale,
                resolution = 20,
                capping= True)
            coil_geo = coil_dis.triangulate()- coil_ic.triangulate()
            #coil.center=(0,0,50)
        self.geo=self.ekran.plotter.add_mesh(coil_geo,color=self.color,opacity=0.75)  # red again
        self.ekran.add_coil(self)
        
        
    def edit_rotation(self,alfa):
        self.alfa=alfa
        Rg=self.get_Rotx(-self.alfa);
        r=np.array([[0],[0],[self.z0]])
        r_=np.dot(Rg,r)
        self.pos=r_
        
    def set_current(self,i):
        self.I=i 
        if self.I>0: 
            self.geo.prop.color='blue'
        elif self.I<0: 
            self.geo.prop.color='orange'
        else: 
            self.geo.prop.color='gray'
        
    def get_Rotx(self,aci):# Derece 
        R=np.array([[1.0,0.0,0.0],
                    [0.0,np.cos(aci*np.pi/180.0),-np.sin(aci*np.pi/180.0)],
                    [0.0,np.sin(aci*np.pi/180.0),np.cos(aci*np.pi/180.0)]])
        return R

    def get_magnetic_field_rotated(self,x,y,z):
        
        Rg=self.get_Rotx(-self.alfa);
        Ri=self.get_Rotx(self.alfa);
        r=np.array([[x],[y],[z]])
        r_=np.dot(Rg,r)
        bb_=self.get_magnetic_field_unrotated(r_[0,0],r_[1,0],r_[2,0])
        b_=np.reshape(bb_[0:3],[-1,1])
        bb=np.dot(Ri, b_)
        bm=np.sqrt(bb[0]**2+bb[1]**2+bb[2]**2)
        b=[bb[0],bb[1],bb[2],bm]
        return np.reshape(b,[-1,])
        
    
    def get_magnetic_field_unrotated(self,x,y,z):  
        z=z-self.z0
        rho2=x**2+y**2;
        r2=x**2+y**2+z**2
        a2=self.a**2
        
        rho=np.sqrt(rho2)
        r=np.sqrt(r2)
        
        alpha2=a2+r2-2*self.a*rho
        beta2=a2+r2+2*self.a*rho
        k2=1-((alpha2)/(beta2))
        gamma=x**2-y**2 
        C=Mu0*self.I*self.N/np.pi 
        
        beta=np.sqrt(beta2)
        
        D=(C/(2*alpha2*beta))
        E_k2=special.ellipe(k2)
        K_k2=special.ellipk(k2)
        
        if rho<self.dl:
            bz=Mu0*self.I*self.N*a2/(2*(a2+z**2)**(3/2))
            bx=0.0; 
            by=0.0;
        else: 
            bz=D*((a2-r2)*E_k2+alpha2*K_k2)
        
            if np.abs(x)<self.dl:
                bx=3*Mu0*self.I*self.N*a2*x*z/(4*(a2+z**2)**(5/2))
            else: 
                bx=D*(x*z/rho2)*((a2+r2)*E_k2-alpha2*K_k2)
            
            if np.abs(y)<self.dl:
                by=3*Mu0*self.I*self.N*a2*y*z/(4*(a2+z**2)**(5/2))
            else: 
                by=D*(y*z/rho2)*((a2+r2)*E_k2-alpha2*K_k2)
    
        
        bm=np.sqrt(bx**2+by**2+bz**2)
        B=[bx,by,bz,bm]
        return B

   

def ornek_fcn(t,X,F):
    return True
