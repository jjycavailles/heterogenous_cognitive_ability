#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:50:07 2020

@author: qwer
"""

import ipywidgets as widgets
from ipywidgets import Layout
import matplotlib.pyplot as plt
#from PIL import Image
from io import BytesIO
import numpy as np

import colorsys
import pickle # package use to save data

from IPython.display import display, Image

#from scipy import interpolate
#import scipy.stats as st

from dynamic import *
import nbinteract as nbi


Model = ["complete", "simplified"]
Plot = ["time series", "histogram"] # "phase portrait", 


class Select_box(widgets.VBox):
    def __init__(self, dashboard):
        
        import numpy as np
        
        self.dashboard = dashboard

        self.selection_model = widgets.Dropdown(options=Model, description = "model")
        self.selection_model.observe(dashboard.on_model_selected, names = "value")

        self.selection_alpha = widgets.FloatSlider(min = 0, max = 1, description = "alpha", value = 0.5)
        self.selection_alpha.observe(dashboard.on_alpha_selected, names = "value")

        self.selection_c = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(10), description = "c")
        self.selection_c.observe(dashboard.on_c_selected, names = "value")

        self.selection_h = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(10), description = "h")
        self.selection_h.observe(dashboard.on_h_selected, names = "value")

        self.selection_l = widgets.FloatLogSlider(min = np.log10(0.1), max = np.log10(10), description = "l")
        self.selection_l.observe(dashboard.on_l_selected, names = "value")

        self.selection_plot = widgets.Dropdown(options=Plot, description = "plot")
        self.selection_plot.observe(dashboard.on_plot_selected, names = "value")

        
        children = [
        self.selection_model,
        self.selection_alpha,
        self.selection_c,
        self.selection_h,
        self.selection_l,
        self.selection_plot,
        ]
        super().__init__(children, layout=Layout(width="100%"))   
        
        

class Image_box(widgets.Box):
    def __init__(self, dashboard):
        #%pip install matplotlib
        import matplotlib.pyplot as plt
        self.image = widgets.Image()
        self.dashboard = dashboard
        
        self.model = self.dashboard.model
        self.alpha = self.dashboard.alpha
        self.c = self.dashboard.c
        self.h = self.dashboard.h
        self.l = self.dashboard.l
        self.plot = self.dashboard.plot
  
        self.print_image()
        
        image_container = widgets.Box([self.image], layout=Layout(width="100%"))
        
        children = [
   #     image_container,
        self.image,   
        ]
        super().__init__(children, layout=Layout(width="100%"))
        
    def print_image(self):
        try:
            import matplotlib.pyplot as plt
        except:
            #%pip install matplotlib -qqq
            import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(10, 6))
        #fig = nbi.plotting.Figure()
        h = self.h
        l = self.l
        alpha = self.alpha
        c = self.c

        #fig = fonction_plot(alpha, c, h, l)

        
        D = Dynamic(h=h, l=l, alpha=alpha, c=c, model=self.model, tFinal=50)
        D.initialisation()
        if(self.plot == "time series"):
            D.eulerEx()
            D.plot(show=False)
            plt.legend(fontsize = 20) # duplicate ...
        elif(self.plot == "phase portrait"):
            D.plot_phase_portrait(show=False)
        elif(self.plot == "histogram"):
            D.plot_histogram(show=False)
            
        image_file = BytesIO()
        fig.savefig(fname = image_file)
        image_file.seek(0)
        image_data = image_file.read()
        self.image.value = image_data
#            self.image.width = 1500
#           self.image.height = 2000
        plt.close()

#          file = open(nom, "rb")
#         image = file.read()
        #plt.imshow(image)
#        self.image.value = image
 #       self.image.format = 'png'


        return
        

    def change_model(self, change):
        self.model = change
        self.print_image()

    def change_alpha(self, change):
        self.alpha = change
        self.print_image()

    def change_c(self, change):
        self.c = change
        self.print_image()
        
    def change_h(self, change):
        self.h = change
        self.print_image()

    def change_l(self, change):
        self.l = change
        self.print_image()

    def change_plot(self, change):
        self.plot = change
        self.print_image()
        
        


