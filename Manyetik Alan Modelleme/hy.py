# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import special


Mu0=4*np.pi*1e-7 # Boşluğun manyetik geçirgenliği 

# Bobin özellikleri 
a=25/1000; # bobin yarıçapı (m) 
N=100 # Bobin sargı sayısı  
I=1 # Akım (A)

# Mıknatıs özellikleri 
m=0.02 ; # manyetik dipol ( ?? )

J=0.0001 # Dönme atalet momenti


#p=np.array([0],[0][0]) 
x=0; y=0.1; z=0.1;

rho2=x**2+y**2;
r2=x**2+y**2+z**2


rho=np.sqrt(rho2)
r=np.sqrt(r2)

alpha2=a**2+r2-2*a*rho
beta2=a**2+r2+2*a*rho
k2=1-((alpha2**2)/(beta2))
gamma=x**2-y**2 
C=Mu0*I/np.pi 

beta=np.sqrt(beta2)

D=(C/(2*alpha2*beta))
E_k2=special.ellipe(k2)
K_k2=special.ellipk(k2)
bx=D*(x*z/rho2)*((a**2+r2)*E_k2-alpha2*K_k2)
by=D*(y*z/rho2)*((a**2+r2)*E_k2-alpha2*K_k2)
bz=D*((a**2-r2)*E_k2+alpha2*K_k2)
bm=np.sqrt(bx**2+by**2+bz**2)
B=[bx,by,bz,bm]


























 


