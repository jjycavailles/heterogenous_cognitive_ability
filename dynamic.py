#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 17:13:15 2020

@author: qwer
"""

import numpy as np
import matplotlib.pyplot as plt



class Dynamic:
    def __init__(self, h,l,alpha,c, tFinal=10):
       self.h = h
       self.l = l
       self.alpha = alpha
       self.c = c
       
       self.Strat = ["ia", "ib", "laa", "lab", "lba", "lbb"]
       
       self.tFinal = tFinal
       self.nbreStep = 1001
       self.T = np.linspace(0, self.tFinal, self.nbreStep)
       
       self.Xb = self.generator_Xb()
       
       return
   
    
    def generator_Xb(self):
        return self.l + (self.h-self.l)*np.random.binomial(n=1, p=self.alpha, size=self.nbreStep)
    
    
    def initialisation(self): #implement other initialisation
        self.X0 = np.zeros(7)+1./7
        return 
    
    
    def get_gamma(self, X, xb):
        if(xb==self.l):
            return X[0] + X[2] + X[3]
        elif(xb==self.h):
            return X[0] + X[2] + X[4]
        else:
            print("problem of value with l and h")
        
    def fitness(self, X, strat, xb):
        gamma = self.get_gamma(X, xb)
        if(strat[0]=="l"): # learn
            if(strat[1::]=="aa"):
                return 1./gamma - self.c
            elif(strat[1::]=="ab"):
                if(xb==self.l):
                    return 1./gamma - self.c
                elif(xb==self.h):
                    return xb/(1-gamma) - self.c
                else:
                    print("problem of value with l and h")
            elif(strat[1::]=="ba"):
                if(xb==self.h):
                    return 1./gamma - self.c
                elif(xb==self.l):
                    return xb/(1-gamma) - self.c
                else:
                    print("problem of value with l and h")
            elif(strat[1::]=="bb"):
                return xb/(1-gamma) - self.c
            else:
                print("Strategies unknown")
        elif(strat[0]=="i"): # ignorant
            if(strat[1]=="a"):
                return 1./gamma
            elif(strat[1]=="b"):
                return float(xb)/(1-gamma)
            else:
                print("Strategies unknown")
        else:
            print("Strategies unknown (learner or ignorant ?)")
        
        
    def phi(self, X, xb):
        """average fitnesss"""
        average = 0
        for i_s, strat in enumerate(self.Strat):
            average += X[i_s]*self.fitness(X, strat, xb)
        return average
        
    def Ft(self, X, xb):
        F = np.zeros(len(X))
        p = self.phi(X, xb)
        for i, (x, strat) in enumerate(zip(X, self.Strat)):
            F[i] = x*(self.fitness(X, strat, xb) - p)
        return F
    
    def eulerEx(self):
        XX = np.zeros((self.nbreStep, len(self.X0)))
        XX[0] = self.X0
        dt = self.T[1] - self.T[0] # for uniform time step !
        for i_t in range(1, len(self.T)):
            xb = self.Xb[i_t] # careful with discretisation 1
            XX[i_t] = XX[i_t-1] + dt * self.Ft(XX[i_t-1], xb)
        self.XX = XX
        #return XX
        
    def plot(self, mode = "all strategies", show = True):
        #plt.figure(figsize = (20, 10))
        if(mode == "all strategies"):            
            for i, strat in enumerate(self.Strat):
                plt.plot(self.T, self.XX[:,i], label = strat)
        elif(mode == "il"):
            plt.plot(self.T, np.sum(self.XX[:,0:2], axis = 1), label = "ignorant")
            plt.plot(self.T, np.sum(self.XX[:,2::], axis = 1), label = "learner")
        else:
            print("What do you want to plot ? (precise mode)")
        plt.legend(fontsize = 30)
        if(show):
            plt.show()
        return
        
    def plot_Xb(self):
        plt.figure(figsize = (20, 5))
        Xb_et = Xb = np.zeros(len(self.Xb)*10)
        for i in range(10):
            Xb_et[i::10] = self.Xb
        plt.plot(np.linspace(self.T[0], self.tFinal, self.nbreStep*10), Xb_et)
        plt.title("Xb", fontsize = 30)
        plt.show()
        