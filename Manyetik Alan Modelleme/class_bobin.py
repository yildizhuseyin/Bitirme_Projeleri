# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 17:55:03 2025

@author: cengiz
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import special


Mu0=4*np.pi*1e-7 # Boşluğun manyetik geçirgenliği 

def ahmet(ad):
    print(ad)
    
class bobin: 
    dl=1e-4
    def __init__(self,a,i=1,n=1,z0=0):
        self.a=a; 
        self.I=i;
        self.N=n; 
        self.z0=z0; 
        
    def get_magnetic_field_un_rotated(self,x,y,z):        
        rho2=x**2+y**2;
        r2=x**2+y**2+z**2
        a2=self.a**2
        
        rho=np.sqrt(rho2)
        r=np.sqrt(r2)
        
        alpha2=self.a**2+r2-2*self.a*rho
        beta2=self.a**2+r2+2*self.a*rho
        k2=1-((alpha2**2)/(beta2))
        gamma=x**2-y**2 
        C=Mu0*self.I*self.N/np.pi 
        
        beta=np.sqrt(beta2)
        
        D=(C/(2*alpha2*beta))
        E_k2=special.ellipe(k2)
        K_k2=special.ellipk(k2)
        
        
        
        if rho<self.dl:
            bz=Mu0*self.I*self.N*a2/(2*(a2+z**2)**(3/2))
        else: 
            bz=D*((self.a**2-r2)*E_k2+alpha2*K_k2)
        
        if np.abs(x)<self.dl:
            bx=3*Mu0*self.I*self.N*a2*x*z/(4*(a2+z**2)**(5/2))
        else: 
            bx=D*(x*z/rho2)*((self.a**2+r2)*E_k2-alpha2*K_k2)
        
        if np.abs(y)<self.dl:
            by=3*Mu0*self.I*self.N*a2*y*z/(4*(a2+z**2)**(5/2))
        else: 
            by=D*(y*z/rho2)*((self.a**2+r2)*E_k2-alpha2*K_k2)
        
        
        bm=np.sqrt(bx**2+by**2+bz**2)
        B=[bx,by,bz,bm]
        return B

   