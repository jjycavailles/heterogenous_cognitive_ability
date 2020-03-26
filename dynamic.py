#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 17:13:15 2020

@author: qwer
"""

import numpy as np
import matplotlib.pyplot as plt



class Dynamic:
    def __init__(self, h,l,alpha,c, model="complete", tFinal=10, nbreStep = 1001):
       self.h = h
       self.l = l
       self.alpha = alpha
       self.c = c
       self.model = model
       
#       self.Strat = ["ia", "ib", "laa", "lab", "lba", "lbb"]
       
       self.tFinal = tFinal
       self.nbreStep = nbreStep
       self.T = np.linspace(0, self.tFinal, self.nbreStep)
       
       self.Xb = self.generator_Xb()
       
       
       if(self.model=="complete"):
           self.Strat = ["ia", "ib", "laa", "lab", "lba", "lbb"]
       elif(self.model=="simplified"):
           self.delta = 1./(1+self.alpha*self.h+(1-self.alpha)*self.l)
           self.Strat = ["ignorant", "learner"]
       else:
           print("Model unknown")
       return
   
    
    def generator_Xb(self):
        #return self.l + (self.h-self.l)*np.random.binomial(n=1, p=self.alpha, size=self.nbreStep)
        return np.random.binomial(n=1, p=self.alpha, size=self.nbreStep)==1 #True if h
    
    def initialisation(self): #implement other initialisation
        if(self.model=="complete"):
            self.X0 = np.zeros(7)+1./7
        elif(self.model=="simplified"):
            self.X0 = np.zeros(2)+1./2
        else:
            print("Model unknown")
        return 
    
    
    def get_gamma(self, X, xb):
        if(self.model=="complete"):
            if(xb):
                return X[0] + X[2] + X[4]
            else:
                return X[0] + X[2] + X[3]            
        elif(self.model=="simplified"):
            if(xb):
                return self.delta*X[0]
            else:
                return self.delta*X[0] + X[1]           
        else:
            print("Model unknown")
        return 
    
    
        
#        else:
 #           print("problem of value with l and h (47)")
        
 
    def fitness(self, X, strat, xb):
        gamma = self.get_gamma(X, xb)
        if(self.model=="complete"): 
            if(strat[0]=="l"): # learn
                if(strat[1::]=="aa"):
                    return 1./gamma - self.c
                elif(strat[1::]=="ab"):
                    if(xb):
                        return xb/(1-gamma) - self.c
                    else:
                        return 1./gamma - self.c
                elif(strat[1::]=="ba"):
                    if(xb):
                        return 1./gamma - self.c
                    else:
                        return xb/(1-gamma) - self.c
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
        elif(self.model=="simplified"):
            if(strat[0]=="i"):
                return self.delta/gamma + (1-self.delta)*float(xb)/(1-gamma)
            elif(strat[0]=="l"):
                if(xb):
                    return xb/(1-gamma) - self.c
                else:
                    return 1./gamma - self.c
            else:
                    print("Strategies unknown")
        else:
            print("Model unknown")
       
        
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
        plt.ylim(0,1)
        if(show):
            plt.show()
        return
        
    def plot_Xb(self):
        plt.figure(figsize = (20, 5))
        Xb_et = np.zeros(len(self.Xb)*10)
        for i in range(10):
            Xb_et[i::10] = self.l + (self.h-self.l)*self.Xb
        plt.plot(np.linspace(self.T[0], self.tFinal, self.nbreStep*10), Xb_et)
        plt.title("Xb", fontsize = 30)
        plt.show()
        
    
    def plot_phase_portrait(self, show=True):
        if(self.model=="complete"): 
            print("Not ready yet, do 3d, triangle or just i and l ...")
        elif(self.model=="simplified"): # make no sense y=1-x ...
            X = np.linspace(0, 1, 31)
            Y = np.linspace(0, 1, 31)
            FX = np.zeros((len(X), len(Y)))
            FY = np.zeros_like(FX)
            for i, x in enumerate(X):
                for j, y in enumerate(Y[::i+1]):            
                    D = Dynamic(h=self.h, l=self.l, alpha=self.alpha, c=self.c, model=self.model, tFinal=0.1, nbreStep = 11)
                    #D.initialisation()
                    D.X0 = [x,y]
                    D.eulerEx()
                    FX[i,j], FY[i,j] = D.XX[-1]
            XX, YY = np.meshgrid(X, Y)
#            plt.contourf(XX, YY, FY)
 #           plt.quiver(XX, YY, FX, FY, color='r')
            plt.streamplot(XX, YY, FX, FY)
        else:
            print("Model unknown")
        if(show):
            plt.show()
        return

    def plot_histogram(self, show=True):
        nbreSimu = 101
        if(self.model=="complete"):
            F = np.zeros((nbreSimu, 7))
            for i in range(nbreSimu):
                D = Dynamic(h=self.h, l=self.l, alpha=self.alpha, c=self.c, model=self.model, tFinal=50, nbreStep = 201)
                #D.initialisation()
                Init = np.random.rand(7)
                D.X0 = Init/sum(Init)
                D.eulerEx()
                F[i,:] = D.XX[-1]              
            for i, strat in enumerate(self.Strat):
                plt.hist(F[:,i], label = strat)
        elif(self.model=="simplified"): # make no sense y=1-x ...
            Y = np.linspace(0,1,nbreSimu)
            FI = np.zeros(nbreSimu)
            FL = np.zeros(nbreSimu)
            for i, y in enumerate(Y):
                D = Dynamic(h=self.h, l=self.l, alpha=self.alpha, c=self.c, model=self.model, tFinal=50, nbreStep = 51)
                #D.initialisation()
                D.X0 = [y, (1-y)]
                D.eulerEx()
                FI[i], FL[i] = D.XX[-1]
            try:
                plt.hist(FI, label = "ignorant")
            except:
                pass
            try:
                plt.hist(FL, label = "learner")
            except:
                pass

        else:
            print("Model unknown")
        plt.legend(fontsize = 20)
        if(show):
            plt.show()
        return



"""
h=10.
l=0.1
alpha=0.5
c=.1
model="simplified"
D = Dynamic(h=h, l=l, alpha=alpha, c=c, model=model, tFinal=50)
D.initialisation()
F = D.plot_histogram()
#D.plot_phase_portrait(show=False)        
"""