# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 22:02:42 2025

@author: pc64x
"""
import numpy as np
import pygame
import random
import math 

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
    
    def draw(self,n=0,t=0,B=[],F=[],T=[]):
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
        self.draw_transparent_text(self.screen,str_n,(850,10),self.DARK_GRAY) 
        self.draw_transparent_text(self.screen,str_time,(950,10),self.DARK_GRAY)
        self.draw_transparent_text(self.screen,str_B,(850,50),self.BLUE)
        self.draw_transparent_text(self.screen,str_F,(850,80),self.RED)
        self.draw_transparent_text(self.screen,str_T,(850,110),self.RED)
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
        for coil in self.coils:
            x=self.zero_point[0]+coil.pos[1]*self.scale[0] 
            y=self.zero_point[1]-coil.pos[2]*self.scale[1]
            line_length = 1000*coil.a
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
            str_X="X: "+str(np.round(robo.X,4))
            str_V="V: "+str(np.round(robo.V,4))
            str_Q="Q: "+str(np.round(robo.Q*180/np.pi,4))
            str_W="W: "+str(np.round(robo.W*180/np.pi,4))
            self.draw_transparent_text(self.screen,str("ROBOT"),(850,200),self.RED)

            self.draw_transparent_text(self.screen,str_X,(850,230),self.RED)
            self.draw_transparent_text(self.screen,str_V,(850,260),self.RED)
            self.draw_transparent_text(self.screen,str_Q,(850,290),self.RED)
            self.draw_transparent_text(self.screen,str_W,(850,320),self.RED)