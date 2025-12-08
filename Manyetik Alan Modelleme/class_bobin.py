# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 17:55:03 2025

@author: cengiz
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import special
from matplotlib import cm


Mu0=4*np.pi*1e-7 # Boşluğun manyetik geçirgenliği 

def ahmet(ad):
    print(ad)
    
class bobin: 
    dl=1e-4
    def __init__(self,a,i=1,n=1,z0=0, alfa=0.0):
        self.a=a; 
        self.I=i;
        self.N=n; 
        self.z0=z0; 
        self.dl= self.a/100
        self.alfa=alfa
        
    def edit_rotation(self,alfa):
        self.alfa=alfa
    def set_current(self,i):
        self.I=i 
        
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

   





######## ÇİZİM FONKSİYONLARI 
def get_random_color():
    r=np.random.random([3,])
    rnd_color=(r[0], r[1], r[2])
    return rnd_color

def plot_list_points_with_length(figNo,subNo,plotList,legend=[],title=None,figsize =(8, 7)):
    level=500;
    fig = plt.figure(figNo,figsize)
    ax = fig.add_subplot(subNo) #♦  projection='3d'
    
    for newData in plotList:
        x,y,color,line_lenght=newData
        if color==None:
            color=get_random_color()
        
        ax.plot(x, y,color,linewidth=line_lenght)
    if not legend==[]:
        ax.legend(legend)
    
    if not title==None:
        ax.set_xlabel('x')
        ax.set_ylabel('Y')
        ax.set_title(title)
        
def plot_list_points(figNo,subNo,plotList,legend=[],title=None,figsize =(8, 7)):
    level=500;
    fig = plt.figure(figNo,figsize)
    ax = fig.add_subplot(subNo) #♦  projection='3d'
    
    for newData in plotList:
        x,y,color=newData
        if color==None:
            color=get_random_color()
        
        ax.plot(x, y,color)
    if not legend==[]:
        ax.legend(legend)
    
    if not title==None:
        ax.set_xlabel('x')
        ax.set_ylabel('Y')
        ax.set_title(title)

def plot_points(figNo,subNo,X,Y,color=None,title=None,figsize =(8, 7)):
    level=500;
    fig = plt.figure(figNo,figsize)
    ax = fig.add_subplot(subNo) #♦  projection='3d'
    if color==None:
        ax.plot(X, Y)
    else: 
        ax.plot(X, Y,color)
    if not title==None:
        ax.set_xlabel('x')
        ax.set_ylabel('Y')
        ax.set_title(title)  
        
def plot_surf_3D(figNo,subNo,X,Y,Z,title):
    # bir veri grubu için yüzey çizimini yapar 
    level=30;
    fig = plt.figure(figNo,figsize =(8, 7))
    ax = fig.add_subplot(subNo,projection='3d') #♦  projection='3d' 
    levels = np.linspace(-1, 1, level)
    # surf=ax.contourf(X, Y, Z, rstride=1, cstride=1, cmap='autumn',
    #     linewidth=0, antialiased=False)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)
    
def plot_surf_2D(figNo,subNo,X,Y,Z,title):
    # bir veri grubu için yüzey çizimini yapar 
    level=30;
    fig = plt.figure(figNo,figsize =(8, 7))
    ax = fig.add_subplot(subNo) #♦  projection='3d' 
    levels = np.linspace(-0.1, 0.1, level)
    surf=ax.contourf(X, Y, Z, cmap='autumn', antialiased=False)
    #surf=ax.contourf(X, Y, Z,[-0.1 -0.05 0.0 0.05 0.1])
    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)

def plot_stream_lines(figNo,subNo,X2D,Y2D,Z2Dx,Z2Dy,title='stream line',Type='linewith',par=0):
    #get_ipython().run_line_magic('matplotlib', 'inline')
    Z=np.sqrt(Z2Dx**2+Z2Dy**2)
    #fig = plt.figure(figsize =(8, 7))
    fig = plt.figure(figNo,figsize =(8, 7))
    ax = fig.add_subplot(subNo) #♦  projection='3d' 
    if Type=='linewith':
        if par==0:
            lw = 5*Z / Z.max()
            strm = ax.streamplot(X2D, Y2D, Z2Dx, Z2Dy, color = Z,
                                  linewidth = lw, cmap ='autumn')
        else:
            strm = ax.streamplot(X2D, Y2D, Z2Dx, Z2Dy, color = Z,
                                  linewidth = 2, cmap ='autumn')
    elif Type=='density':
        if par==0:
            par=[0.1, 0.9]
        strm = ax.streamplot(X2D, Y2D, Z2Dx, Z2Dy, color = Z,
                              density=par, cmap ='autumn')
    fig.colorbar(strm.lines)
    plt.tight_layout() # show plot
    plt.xlabel('X');    plt.ylabel('Y'); plt.title(title)
    plt.show();  

def plot_vector_2D(figNo,subNo,X,Y,U,V,scale=1,title='vector'):
    # bir veri grubu için yüzey çizimini yapar 
    level=30;
    fig = plt.figure(figNo,figsize =(8, 7))
    ax = fig.add_subplot(subNo) #♦  projection='3d' 
    ax.quiver(X, Y, U, V, color='b', units='xy', scale=scale)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)
    