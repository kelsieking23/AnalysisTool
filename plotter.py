import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import pandas as pd
import sys
import argparse
import json
from tkinter import *
from tkinter import filedialog
import os
import numpy as np
import subprocess
from gui import Batch, Timeseries

class Plotter:

    def __init__(self, **params):
    
        # set default options to None
        self.files = []
        self.title = None
        self.subtitle = None
        self.save_path = None
        self.colors = []
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        self.xlabel = None
        self.ylabel = None
        self.majorxticks = None
        self.majoryticks = None
        self.minorxticks = None
        self.minoryticks = None
        self.font = None
        self.xlabel_font_size = None
        self.ylabel_font_size = None
        self.xtick_font_size = None
        self.ytick_font_size = None
        self.alter_xscale = None
        self.alter_yscale = None

        # change attributes based on user input
        for key in params.keys():
            self.__setattr__(key,params[key])

        print(self.__dict__)

    # accessory function
    def divide(self, n, m):
        if n / m > 10:
            return self.divide(n, m*10)
        else:
            return m

    def alter_timescale(self, axis, dfs):
        time_conversions = {
            '\u03BCs': 1E-6,
            'ns': 1E-9,
            'ps': 1E-12
        }
        new_dfs = []
        if axis == 'X':
            convert_from = self.alter_xscale[0]
            convert_to = self.alter_xscale[1]
            conversion_factor = time_conversions[convert_to] / time_conversions[convert_from]
            for df in dfs:
                df['X'] = df['X'] / conversion_factor
                new_dfs.append(df)
        return new_dfs


    def timeseries(self):

        # set color cycle
        if self.colors != []:
            i = 0
            for item in self.colors:
                new_item = self.colors[i].strip()
                if '#' in new_item[0]:
                    new_item = new_item[1:]
                self.colors[i] = new_item


            mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=self.colors)

        # put xvgs into dataframes
        dfs = []
        files = list(self.files)
        for filename in files:
            print(filename)
            skiprows = 0
            f = open(filename, 'r')
            for line in f:
                line_parts = line.split()
                for part in line_parts:
                    if '@' in part:
                        skiprows += 1
                        break
                    if '#' in part:
                        skiprows += 1
                        break
                else:
                    df = pd.read_csv(filename, skiprows=skiprows, delim_whitespace=True, names=['X','Y'])
                    dfs.append(df)
                    f.close()
                    break
        
        if self.alter_xscale is not None:
            dfs = self.alter_timescale(axis='X', dfs=dfs)
        if self.alter_yscale is not None:
            dfs = self.alter_timescale(axis='Y', dfs=dfs)


        #plot dataframes
        for df in dfs:
            print(df.tail())
            x = df['X']
            y = df['Y']
            plt.plot(x, y)
    
        # set graph parameters
        ax = plt.axes() # initialize axes object

        df = dfs[0]
        # establish graph min and max 
        if self.xmin is None:
            self.xmin = int(df.iloc[0][0].round())
        if self.xmax is None:
            self.xmax = int(df['X'].iloc[-1].round())


        x_range = np.arange(self.xmin, self.xmax+1, self.divide(self.xmax, 10))

        xlocs, xlabels = plt.xticks() # get current xtick locations and labels
        ylocs, ylabels = plt.yticks() # get current ytick locations and labels

        if self.majorxticks is not None:
            ax.xaxis.set_major_locator(MultipleLocator(float(self.majorxticks)))
        else:
            plt.xticks(xlocs[1:], x_range)

        if self.majoryticks is not None:
            ax.yaxis.set_major_locator(MultipleLocator(float(self.majoryticks)))

        if self.minorxticks is not None:
            ax.xaxis.set_minor_locator(MultipleLocator(float(self.minorxticks))) # set minor x tick labels
        
        if self.minoryticks is not None:
            ax.yaxis.set_minor_locator(MultipleLocator(float(self.minoryticks))) # set minor y tick labels
        
        # tick label size
        ax.tick_params(axis='x',labelsize=float(self.xtick_font_size)) 
        ax.tick_params(axis='y', labelsize=float(self.ytick_font_size))

        ymin, ymax = plt.ylim()
        if self.ymin is not None:
            if self.ymax is not None:
                plt.ylim(float(self.ymin), float(self.ymax))
            else:
                plt.ylim(float(self.ymin), ymax )
        if self.ymax is not None:
            plt.ylim(ymin, float(self.ymax))
            
            
        if self.xmin is not None:
            if self.xmax is not None:
                plt.xlim(float(self.xmin), float(self.xmax))
            else:
                plt.xlim(float(self.xmin), df['X'].iloc[-1])
        else:
            if self.xmax is not None:
                plt.xlim(df['X'].iloc[0], float(self.xmax))
            else:
                plt.xlim(df['X'].iloc[0], df['X'].iloc[-1])

        if self.xlabel is not None:
            plt.xlabel(self.xlabel, fontsize=float(self.xlabel_font_size), fontname=self.font) # x axis label
        if self.ylabel is not None:
            plt.ylabel(self.ylabel, fontsize=float(self.ylabel_font_size), fontname=self.font) # y axis label
        
        if self.title is not None:
            if self.subtitle is not None:
                title = plt.suptitle(self.title, fontname=self.font, fontsize=float(self.title_font_size))
                subtitle = plt.title(self.subtitle, fontname=self.font, fontsize=float(self.subtitle_font_size))
            else:
                title = plt.title(self.title, fontname=self.font, fontsize=float(self.title_font_size))
            
        plt.savefig(self.save_path, dpi=300) # save figure to .png
        
        plt.show()

        