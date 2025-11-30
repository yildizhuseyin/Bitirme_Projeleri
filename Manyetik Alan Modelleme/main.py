# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 17:53:49 2025

@author: cengiz
"""


from class_bobin import *



# Bobin özellikleri 
a=100/1000; # bobin yarıçapı (m) 
N=100 # Bobin sargı sayısı  
I=1 # Akım (A)

# Mıknatıs özellikleri 
m=0.02 ; # manyetik dipol ( ?? )

J=0.0001 # Dönme atalet momenti

bobin0=bobin(a,i=10)
bobin1=bobin(a,i=10,z0=a/2)
bobin2=bobin(a,i=10,z0=a/2,alfa=90.0)


#p=np.array([0],[0][0]) 
x=0; y=0.1; z=0.1;

b=bobin1.get_magnetic_field_unrotated(x, y, z)


"""
# 1 boyutta manyetik alan 
Y=np.linspace(-2*a, 2*a,20)
#B=np.zeros_like(Y)
B=np.zeros([len(Y),4])

for i in range(len(Y)):
    b=bobin1.get_magnetic_field_unrotated(x, Y[i], z)
    B[i,:]=b[:]
    

fig, ax = plt.subplots()
ax.plot(Y, B[:,3],'-k')
#ax.set(xlim=(-10, 10), xlabel="t")
ax.legend(fontsize=14)
plt.show()
"""
x=0.0
n=50;  m=1*n; 
L=3*a; W=L;
y=np.linspace(-L,L,n)
z=np.linspace(-W,W,m)

Y2D,Z2D=np.meshgrid(y,z)

B2D=np.zeros([m,n,4])
B2D_2=np.zeros([m,n,4])

#B=np.zeros([X2D.shape[0],X2D.shape[1],4])

for j in range(m):
    for i in range(n):
        b=bobin1.get_magnetic_field_unrotated(x,Y2D[j,i], Z2D[j,i])
        B2D[j,i,:]=b[:]
        b_2=bobin2.get_magnetic_field_rotated(x,Y2D[j,i], Z2D[j,i])
        B2D_2[j,i,:]=b_2[:]


plot_surf_2D(2,131,Y2D,Z2D,B2D[:,:,3],'B')
plot_stream_lines(2,132,Y2D,Z2D,B2D[:,:,1],B2D[:,:,2],title='stream line')
plot_vector_2D(2,133,Y2D,Z2D,B2D[:,:,1],B2D[:,:,2],scale=1e-2,title='vector')
    
plot_surf_2D(3,131,Y2D,Z2D,B2D_2[:,:,3],'B')
plot_stream_lines(3,132,Y2D,Z2D,B2D_2[:,:,1],B2D_2[:,:,2],title='stream line')
plot_vector_2D(3,133,Y2D,Z2D,B2D_2[:,:,1],B2D_2[:,:,2],scale=1e-2,title='vector')