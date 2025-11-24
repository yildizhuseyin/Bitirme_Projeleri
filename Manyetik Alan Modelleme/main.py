# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 17:53:49 2025

@author: cengiz
"""


from class_bobin import *



# Bobin özellikleri 
a=25/1000; # bobin yarıçapı (m) 
N=100 # Bobin sargı sayısı  
I=1 # Akım (A)

# Mıknatıs özellikleri 
m=0.02 ; # manyetik dipol ( ?? )

J=0.0001 # Dönme atalet momenti


bobin1=bobin(a,i=10)

#p=np.array([0],[0][0]) 
x=0; y=0.1; z=0.1;

b=bobin1.get_magnetic_field_un_rotated(x, y, z)

Y=np.linspace(-2*a, 2*a,20)
#B=np.zeros_like(Y)
B=np.zeros([len(Y),4])

for i in range(len(Y)):
    b=bobin1.get_magnetic_field_un_rotated(x, Y[i], z)
    B[i,:]=b[:]
    

fig, ax = plt.subplots()
ax.plot(Y, B[:,3],'-k')
#ax.set(xlim=(-10, 10), xlabel="t")
ax.legend(fontsize=14)
plt.show()
    