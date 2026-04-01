# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 03:15:04 2025

@author: pc64x
"""

import numpy as np
import random
import math 




class on_of_controller_1D:
    
    def __init__(self,dt,y_ref,delta=1,scale=1):
        self.e=0 
        self.scale=scale
        self.delta=delta
        self.out=0
        
    def set_referance(self,yref):
        self.y_ref=yref
        
    def set_parameters(self,scale,delta=None): 
        self.scale=scale
        if not delta==None: 
            self.delta=delta
    
    def apply_with_err(self,e):
        self.e=e
        if self.e>self.delta:
            self.out=0
        elif self.e<-self.delta:
            self.out=1*self.scale
        return self.out
    
    def apply(self,y):
        self.e=self.yref-y 
        if self.e>self.delta:
            self.out=0
        elif self.e<-self.delta:
            self.out=1*self.scale
        return self.out
        

        

class PID_controller_1D:
    
    def __init__(self,dt,y_ref, kp=1.0,kd=0.0,ki=0.0):
        self.kp=kp
        self.kd=kd
        self.ki=ki
        self.dt=dt
        self.e=0.0 
        self.e_=0.0
        self.I_e=0.0
        self.de=0.0
        self.y_ref=y_ref 
        self.out=0.0
        self.scale_factor=np.array([1.0,1.0,1.0])
        
    def set_referance(self,yref):
        self.y_ref=yref
        
    def set_parameters(self,kp,kd=0.0,ki=0.0): 
        self.kp=kp
        self.kd=kd
        self.ki=ki
    
    def set_scale_factor(self,scale_factor):
        self.scale_factor=np.array(scale_factor)
        
    def set_ZNC(self,kc,tc,Type='PID'):
        if Type=='PID':
            self.kp=0.6*kc*self.scale_factor[0]
            self.ki=1*1.2*kc/tc*self.scale_factor[1]
            self.kd=1.0*0.075*kc*tc*self.scale_factor[2]
        elif Type=='PD':
            self.kp=0.8*kc*self.scale_factor[0]
            self.ki=0
            self.kd=1.0*0.1*kc*tc*self.scale_factor[2]
        elif Type=='PI':
            self.kp=0.45*kc*self.scale_factor[0]
            self.ki=1*0.54*kc/tc*self.scale_factor[1]
            self.kd=0.0
        elif Type=='P':
            self.kp=1.0*kc*self.scale_factor[0]
            self.ki=0
            self.kd=0.0
            
    def apply_with_err(self,e):
        self.e=e
        self.apply_derivative()
        self.apply_integral()
        self.out=self.kp*self.e+self.kd*self.de+self.ki*self.I_e
        self.e_=self.e
        return self.out
    
    def apply(self,y):
        self.e=self.y_ref-y 
        self.apply_derivative()
        self.apply_integral()
        self.out=self.kp*self.e+self.kd*self.de+self.ki*self.I_e
        self.e_=self.e
        return self.out
    
    def apply_with_ref(self,y,y_ref):
        self.e=y_ref-y 
        self.apply_derivative()
        self.apply_integral()
        self.out=self.kp*self.e+self.kd*self.de+self.ki*self.I_e
        self.e_=self.e
        return self.out
        
    def apply_derivative(self):
        self.de=self.e/self.dt
    
    def apply_integral(self):
        self.I_e=self.I_e+0.5*(self.e+self.e_)*self.dt
        