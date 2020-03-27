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
import plotter
from PIL import Image, ImageTk
import ToolTips

class App(Tk): # used to be class App(Tk):
    def __init__(self):
        Tk.__init__(self) 

        # set geometry
        self.geometry('1500x400')
        # initialize toolbar
        menubar = Toolbar(self.master)
        self.config(menu=menubar)

        # title screen
        title = Label(self, text='Bevan & Brown Lab Analysis Tool')
        title.configure(font=('Arial', 20))
        title.pack()
        load = Image.open('imgs/logo.png')
        resize = load.resize((375, 105), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resize)
        img = Label(self, image=render)
        img.image = render
        img.pack()

        # buttons
        batch_button = Button(self, text='Create Batch', command=self.create_batch)
        batch_button.pack()

    def create_batch(self):
        window = BatchWindow(self)
    
class Toolbar(Menu):
    def __init__(self, master):
        # initialize menu
        Menu.__init__(self, master)
        filemenu = Menu(self)

        # add file cascade
        self.add_cascade(label='Plot', menu=filemenu)
        filemenu.add_command(label='Import data...', command=self.file_import)
        filemenu.add_command(label='Create batch...', command=self.create_batch)
    
    # import files
    def file_import(self):
        files = filedialog.askopenfilenames(initialdir = os.getcwd(),title = "Select file",filetypes = (("xvg files","*.xvg"),("dat files","*.dat"),("all files","*.*")))
        self.master.files = files

    # create an instance of BatchWindow
    def create_batch(self):
        window = BatchWindow(self.master)

class Timeseries:
    def __init__(self, **params):
        
        self.files = None
        self.title = None
        self.subtitle = None
        self.save_path = None

class Batch:
    def __init__(self, **params):

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
        self.alter_yscale = None
        self.alter_xscale = None
        self.linewidth = None
        self.secondary_x = None
        self.secondary_y = None
        self.direction = None

        # create a list to hold TimeSeries objects
        self.timeseries_batch = []
        # create a TimeSeries object corresponding to the first feild entry row in the window, and add to list
        plot = Timeseries()
        self.timeseries_batch.append(plot)
    
    def run(self):
        for timeseries in self.timeseries_batch:
            plot = plotter.Plotter(files=timeseries.files, title=timeseries.title, subtitle=timeseries.subtitle, save_path=timeseries.save_path, colors=self.colors,
                                    xmin=self.xmin, xmax=self.xmax, ymin=self.ymin, ymax=self.ymax, xlabel=self.xlabel, ylabel=self.ylabel, majorxticks=self.majorxticks,
                                    majoryticks=self.majoryticks, minorxticks=self.minorxticks, minoryticks=self.minoryticks, font=self.font, xlabel_font_size=self.xlabel_font_size,
                                    ylabel_font_size=self.ylabel_font_size, xtick_font_size=self.xtick_font_size, ytick_font_size=self.ytick_font_size, alter_xscale=self.alter_xscale, 
                                    alter_yscale=self.alter_yscale, linewidth=self.linewidth, secondary_x=self.secondary_x, secondary_y=self.secondary_y, direction=self.direction)
            plot.timeseries()

    def add_timeseries(self):
        plot = Timeseries()
        self.timeseries_batch.append(plot)

class BatchWindow(Toplevel):
    def __init__(self, master, batch=None):
        # initalize holder variables
        self.master = master
        self.batch = Batch() # create a Batch object to hold data related to project
        self.filelabel = None
        self.row = 2 # to keep track of rows on grid to dynamically add group entry feilds
        self.group = 1 # to keep track of groups added to dynamically add group entry feilds
        self.column = 2 # to keep track columns on grid to dynamically add color entries
        self.colorrow = 5 # same as above


        # initialize window
        self.window = Toplevel(self.master)
        # self.window.geometry('2000x500')
        
        # initialize all frames
        # master frame
        frame = Frame(self.window)
        frame.pack()

        # title frame
        title_frame = Frame(self.window)
        title_frame.pack(anchor=W)

        # button frame and feild entry frames
        self.group_entry_frame = LabelFrame(self.window)
        self.group_entry_frame.pack(fill='both')
        
        # button holder 
        self.button_holder = Frame(self.window)
        self.button_holder.pack()

        # add grah parameters frame
        batch_params_frame = Frame(self.window)
        batch_params_frame.pack()

        # add general and axes parameters frames
        self.general_params_frame = LabelFrame(batch_params_frame)
        self.general_params_frame.pack(side=TOP, anchor=W, fill='both')
        self.axes_params_frame = Frame(batch_params_frame)
        self.axes_params_frame.pack(side=BOTTOM)

        # add x and y ax parameters frames
        self.x_ax_params_frame = LabelFrame(self.axes_params_frame)
        self.x_ax_params_frame.pack(side=LEFT)
        self.y_ax_params_frame = LabelFrame(self.axes_params_frame)
        self.y_ax_params_frame.pack(side=RIGHT)

        # add button holding frame for bottom
        button_frame = Frame(self.window)
        button_frame.pack()
        
        # title
        label = Label(title_frame, text='Create Batch')
        label.configure(font=('Arial', 20))
        label.grid(row=0, column=0, sticky=W, pady=2)
        info = Label(title_frame, text='Feilds marked with an asteriks (*) are optional')
        info.configure(font=('Arial', 15))
        info.grid(row=1, column=0, pady=2)

        # "add group" and "clear selection" buttons
        button_group_entry_frame = Frame(self.group_entry_frame)
        button_group_entry_frame.pack(side=TOP, anchor=W)
        self.field_entry_frame = Frame(self.group_entry_frame)
        self.field_entry_frame.pack(side=BOTTOM, anchor=W)

        Button(button_group_entry_frame, text='Add Group', command=self.add_group).grid(row=0, column=0, pady=2)
        Button(button_group_entry_frame, text='Clear Selection', command=self.clear_selection).grid(row=0, column=1, pady=2)
        Button(button_group_entry_frame, text='Delete Selection', command=self.delete_selection).grid(row=0, column=2, pady=2)


        # initialize first row of group entry feilds
        feild_frame = Frame(self.field_entry_frame)
        feild_frame.pack()
        var = IntVar()
        
        sele = Checkbutton(feild_frame, variable=var)
        sele.grid(row=2, column=0, pady=2)
        sele.var = var

        group_stringvar = StringVar()
        group_stringvar.set('Group 1')
        group_label = Label(feild_frame, textvariable=group_stringvar)
        group_label.grid(row=2, column=1, pady=2)
        group_label.var = group_stringvar

        files_label = Label(feild_frame, text='Files:')
        files_label.grid(row=2, column=2, pady=2)
        
        file_import_button = Button(feild_frame, text='Import files', command=self.file_import_wrapper(feild_frame))
        file_import_button.grid(row=2, column=3, pady=2)

        filelistvar = StringVar()
        filelistvar.set('               (No files imported)               ')
        files_list = Label(feild_frame, textvariable=filelistvar)
        files_list.grid(row=2, column=4, pady=2)
        files_list.var = filelistvar

        alt_suptitle_label = Label(feild_frame, text='*Title:')
        alt_suptitle_label.grid(row=self.row, column=5, pady=2)

        alt_suptitle_entry = Entry(feild_frame)
        alt_suptitle_entry.grid(row=self.row,column=6, pady=2)

        alt_subtitle_label = Label(feild_frame, text='*Subtitle:')
        alt_subtitle_label.grid(row=self.row, column=7, pady=2)

        alt_subtitle_entry = Entry(feild_frame)
        alt_subtitle_entry.grid(row=self.row, column=8, pady=2)

        savedest_button = Button(feild_frame, text='Save as...', command=self.savedest_wrapper(feild_frame))
        savedest_button.grid(row=self.row, column=9, pady=2)


        # add general parameters entry feilds (colors, font, line width)
        gen_label = Label(self.general_params_frame, text='General Graph Parameters')
        gen_label.configure(font=('Arial', 17))
        gen_label.grid(row=0, column=0, pady=5)
        
        Label(self.general_params_frame, text='Font:').grid(row=2, column=0, pady=2, sticky=W)
        font_options = ['Helvetica', 'Arial', 'Matploblib Default']
        self.fontvar = StringVar(self.general_params_frame)
        self.fontvar.set('Helvetica')
        font_menu = OptionMenu(self.general_params_frame, self.fontvar, *font_options)
        font_menu.grid(row=2, column=1, pady=2, sticky=W)

        Label(self.general_params_frame, text='*Adjust line width:').grid(row=3, column=0, pady=2, sticky=W)
        self.linewidth_var = IntVar()
        self.linewidth_var.set(1)
        linewidth_entry = Entry(self.general_params_frame, text=self.linewidth_var, width=6).grid(row=3, column=1, pady=2, sticky=W)
        
        self.direction_var = IntVar()
        self.direction_var.set(1)
        Label(self.general_params_frame, text='Tick marks point:').grid(row=4, column=0, pady=2, sticky=W)
        Radiobutton(self.general_params_frame, text='Out', variable=self.direction_var, value=1).grid(row=4, column=1, pady=2, sticky=W)
        Radiobutton(self.general_params_frame, text='In', variable=self.direction_var, value=2).grid(row=4, column=2, pady=2, sticky=W)

        Label(self.general_params_frame, text='*Colors (enter HEX values):').grid(row=5, column=0, pady=2, sticky=W)
        Button(self.general_params_frame, text='Add color', command=self.add_color).grid(row=5, column=1, pady=2, sticky=W)

        # add batch params feilds
        # x properties
        x_properties = Label(self.x_ax_params_frame, text='X-axis properties (all paramaters optional)')
        x_properties.configure(font=('Arial', 17))
        x_properties.grid(row=0, column=0, pady=5)

        x_ax_limits = Label(self.x_ax_params_frame, text='Axis Limits')
        x_ax_limits.configure(font=('Arial', 15))
        x_ax_limits.grid(row=1, column=0, pady=5, sticky=W)

        Label(self.x_ax_params_frame, text='Lower limit:').grid(row=2, column=0, pady=2, sticky=E)
        Entry(self.x_ax_params_frame).grid(row=2, column=1, pady=2)
        Label(self.x_ax_params_frame, text='Upper limit:').grid(row=2, column=2, pady=2, sticky=E)
        Entry(self.x_ax_params_frame).grid(row=2, column=3, pady=2)

        x_ax_spacing = Label(self.x_ax_params_frame, text='Tickmarks and Labels')
        x_ax_spacing.configure(font=('Arial', 15))
        x_ax_spacing.grid(row=3, column=0, pady=5, sticky=W)

        Label(self.x_ax_params_frame, text='Major tickmark spacing:').grid(row=4, column=0, pady=2, sticky=E)
        Entry(self.x_ax_params_frame).grid(row=4, column=1, pady=2)
        Label(self.x_ax_params_frame, text='Minor tickmark spacing:').grid(row=4, column=2, pady=2, sticky=E)
        Entry(self.x_ax_params_frame).grid(row=4, column=3, pady=2)

        Label(self.x_ax_params_frame, text='Tick label font size:').grid(row=5, column=0, pady=2, sticky=E)
        Entry(self.x_ax_params_frame).grid(row=5, column=1, pady=2)

        self.top_var = IntVar()
        self.top_var.set(0)
        Label(self.x_ax_params_frame, text='Show tickmarks on top:').grid(row=6, column=0, pady=2, sticky=E)
        Checkbutton(self.x_ax_params_frame, variable=self.top_var).grid(row=6, column=1, pady=2, sticky=W)

        x_ax_title = Label(self.x_ax_params_frame, text='Title properties')
        x_ax_title.configure(font=('Arial', 15))
        x_ax_title.grid(row=7, column=0, pady=5, sticky=W)

        Label(self.x_ax_params_frame, text='Axis label:').grid(row=8, column=0, pady=2, sticky=E)
        Entry(self.x_ax_params_frame).grid(row=8, column=1, pady=2)

        Label(self.x_ax_params_frame, text='Axis label font size:').grid(row=8, column=2, pady=2, sticky=E)
        Entry(self.x_ax_params_frame).grid(row=8, column=3, pady=2)

        xscale = Label(self.x_ax_params_frame, text='Axis scale')
        xscale.configure(font=('Arial', 15))
        xscale.grid(row=9, column=0, pady=5, sticky=W)

        Label(self.x_ax_params_frame, text='Current scale:').grid(row=10, column=0, pady=2, sticky=E)
        
        self.xscale_stringvar_actual = StringVar()
        self.xscale_stringvar = StringVar()
        self.xscale_stringvar.set('(Import files to detect axis scale)')
        self.xscale_stringvar_actual.set('(Import files to detect axis scale)')
        current_xscale = Label(self.x_ax_params_frame, textvariable=self.xscale_stringvar_actual)
        current_xscale.grid(row=10, column=1, pady=2, sticky=E)
        current_xscale.var = self.xscale_stringvar

        Label(self.x_ax_params_frame, text='Convert to...').grid(row=10, column=2, pady=2, sticky=E)

        scale_conversions = ['(Import files to detect axis scale)']
        self.xscale_menu = OptionMenu(self.x_ax_params_frame, self.xscale_stringvar, scale_conversions)
        self.xscale_menu.grid(row=10, column=3, pady=2, sticky=E)

        # y properties
        y_properties = Label(self.y_ax_params_frame, text='Y-axis properties (all parameters optional)')
        y_properties.configure(font=('Arial', 17))
        y_properties.grid(row=0, column=0, pady=5)

        y_ax_limits = Label(self.y_ax_params_frame, text='Axis Limits')
        y_ax_limits.configure(font=('Arial', 15))
        y_ax_limits.grid(row=1, column=0, pady=5, sticky=W)

        Label(self.y_ax_params_frame, text='Lower limit:').grid(row=2, column=0, pady=2, sticky=E)
        Entry(self.y_ax_params_frame).grid(row=2, column=1, pady=2)
        Label(self.y_ax_params_frame, text='Upper limit:').grid(row=2, column=2, pady=2, sticky=E)
        Entry(self.y_ax_params_frame).grid(row=2, column=3, pady=2)

        y_ax_spacing = Label(self.y_ax_params_frame, text='Tickmarks and Labels')
        y_ax_spacing.configure(font=('Arial', 15))
        y_ax_spacing.grid(row=3, column=0, pady=5, sticky=W)

        Label(self.y_ax_params_frame, text='Major tickmark spacing:').grid(row=4, column=0, pady=2, sticky=E)
        Entry(self.y_ax_params_frame).grid(row=4, column=1, pady=2)
        Label(self.y_ax_params_frame, text='Minor tickmark spacing:').grid(row=4, column=2, pady=2, sticky=E)
        Entry(self.y_ax_params_frame).grid(row=4, column=3, pady=2)

        Label(self.y_ax_params_frame, text='Tick label font size:').grid(row=5, column=0, pady=2, sticky=E)
        Entry(self.y_ax_params_frame).grid(row=5, column=1, pady=2)

        self.right_var = IntVar()
        self.right_var.set(0)
        Label(self.y_ax_params_frame, text='Show tickmarks on the right:').grid(row=6, column=0, pady=2, sticky=E)
        Checkbutton(self.y_ax_params_frame, variable=self.right_var).grid(row=6, column=1, pady=2, sticky=W)

        y_ax_title = Label(self.y_ax_params_frame, text='Title properties')
        y_ax_title.configure(font=('Arial', 15))
        y_ax_title.grid(row=7, column=0, pady=5, sticky=W)

        Label(self.y_ax_params_frame, text='Axis label:').grid(row=8, column=0, pady=2, sticky=E)
        Entry(self.y_ax_params_frame).grid(row=8, column=1, pady=2)

        Label(self.y_ax_params_frame, text='Axis label font size:').grid(row=8, column=2, pady=2, sticky=E)
        Entry(self.y_ax_params_frame).grid(row=8, column=3, pady=2)

        yscale = Label(self.y_ax_params_frame, text='Axis scale')
        yscale.configure(font=('Arial', 15))
        yscale.grid(row=9, column=0, pady=5, sticky=W)

        Label(self.y_ax_params_frame, text='Current scale:').grid(row=10, column=0, pady=2, sticky=E)

        self.yscale_stringvar_actual = StringVar()
        self.yscale_stringvar = StringVar()
        self.yscale_stringvar.set('(Import files to detect axis scale)')
        self.yscale_stringvar_actual.set('(Import files to detect axis scale)')
        current_yscale = Label(self.y_ax_params_frame, textvariable=self.yscale_stringvar_actual)
        current_yscale.grid(row=10, column=1, pady=2, sticky=E)
        current_yscale.var = self.yscale_stringvar

        Label(self.y_ax_params_frame, text='Convert to...').grid(row=10, column=2, pady=2, sticky=E)

        self.yscale_menu = OptionMenu(self.y_ax_params_frame, self.yscale_stringvar, scale_conversions)
        self.yscale_menu.grid(row=10, column=3, pady=2, sticky=E)


        # run and save buttons
        run_batch_button = Button(button_frame, text='Run Batch', command=self.run)
        run_batch_button.grid(row=8, column=4, pady=2, sticky=W)

        Button(button_frame, text='Save Batch Parameters', command=self.save_batch).grid(row=8, column=5, pady=2)

    # import files for a group
    def file_import_wrapper(self, frame):
        def file_import(frame=frame):
            # open files
            files = filedialog.askopenfilenames(initialdir = os.getcwd(),title = "Select file",filetypes = (("xvg files","*.xvg"),("dat files","*.dat"),("all files","*.*")))
            # update batch constuctor
            if files != '':
                for item in frame.winfo_children():
                    dic = item.__dict__
                    if dic['_name'] == '!label':
                        groupid = item.var.get()
                        groupid = groupid.split()[1]
                        groupid = int(groupid) - 1
                        self.batch.timeseries_batch[groupid].files = files
                #create lists for ToolTips
                widgets = []
                text = []
                # get the string of file names from list; create truncated string if it will take up too much space
                liststring = str(files)
                if len(liststring) > 40:
                    trunc_label = liststring[0:33] + '...'
                    # get the current file label (specifically, the StringVar associated w/ it) to change the value
                    for obj in frame.winfo_children():
                        dic = obj.__dict__
                        if '!label3' in dic['_name']:
                            obj.var.set(trunc_label)
                            text.append(liststring)
                            widgets.append(obj)
                    # ToolTips is a script from github (that i edited to fix some problems) that creates a tool tip upon hovering
                    tooltips_obj = ToolTips.ToolTips(widgets, text)
                else:
                    label = Label(frame, text=liststring)
                    label.grid(row=self.row, column=4, pady=2)
                if len(self.batch.timeseries_batch) == 1:
                    self.detect_axes_scale(files)
        return file_import

    def detect_axes_scale(self, files):
        f = open(files[0], 'r')
        i = 0
        # identify the axis from the xvg file
        for line in f:
            if 'xaxis' in line:
                string = ''
                line_parts = line.split()
                unit = line_parts[4]
                for char in unit:
                    if not char.isalnum():
                        continue
                    else:
                        string = string + char   
                self.xscale_stringvar_actual.set(string)
                self.xscale_stringvar.set(string)   
            if 'yaxis' in line:
                string = ''
                line_parts = line.split()
                unit = line_parts[4]
                for char in unit:
                    if not char.isalnum():
                        continue
                    else:
                        string = string + char
                self.yscale_stringvar_actual.set(string)
                self.yscale_stringvar.set(string)    
            if i == 30:
                f.close()
                break
            i += 1

        # create appropriate option menus
        self.xscale_menu.destroy()
        xscale_conversions = ['ps', 'ns', '\u03BCs']
        self.xscale_menu = OptionMenu(self.x_ax_params_frame, self.xscale_stringvar, *xscale_conversions)
        self.xscale_menu.grid(row=9, column=3, pady=2, sticky=E)
        
        self.yscale_menu.destroy()
        yscale_conversions = ['nm', 'pm', '\u03BCm']
        self.yscale_menu = OptionMenu(self.y_ax_params_frame, self.yscale_stringvar, *yscale_conversions)
        self.yscale_menu.grid(row=9, column=3, pady=2, sticky=E)

    def savedest_wrapper(self, frame):
        def savedest(frame=frame):
            dir_name = filedialog.asksaveasfilename()
            if dir_name != '':
                for item in frame.winfo_children():
                    dic = item.__dict__
                    if dic['_name'] == '!label':
                        groupid = item.var.get()
                        groupid = groupid.split()[1]
                        groupid = int(groupid) - 1
                        self.batch.timeseries_batch[groupid].save_path = dir_name
                Label(frame, text=dir_name).grid(row=self.row, column=10, pady=2)
        return savedest
    
    # add a group feild
    def add_group(self):
        feild_frame = Frame(self.field_entry_frame)
        feild_frame.pack(anchor=W)

        var = IntVar()
        sele = Checkbutton(feild_frame, variable=var)
        sele.grid(row=self.row, column=0, pady=2)
        sele.var = var

        self.group = self.group + 1 
        group_text = 'Group ' + str(self.group)
        group_stringvar = StringVar()
        group_stringvar.set(group_text)
        group_label = Label(feild_frame, textvariable=group_stringvar)
        group_label.grid(row=self.row, column=1, pady=2)
        group_label.var = group_stringvar

        files_label = Label(feild_frame, text='Files:')
        files_label.grid(row=self.row, column=2, pady=2)

        file_import_button = Button(feild_frame, text='Import files', command=self.file_import_wrapper(feild_frame))
        file_import_button.grid(row=self.row, column=3, pady=2)

        filelistvar = StringVar()
        filelistvar.set('               (No files imported)               ')
        files_list = Label(feild_frame, textvariable=filelistvar)
        files_list.grid(row=2, column=4, pady=2)
        files_list.var = filelistvar

        alt_suptitle_label = Label(feild_frame, text='*Title:')
        alt_suptitle_label.grid(row=self.row, column=5, pady=2)

        alt_suptitle_entry = Entry(feild_frame)
        alt_suptitle_entry.grid(row=self.row,column=6, pady=2)

        alt_subtitle_label = Label(feild_frame, text='*Subtitle:')
        alt_subtitle_label.grid(row=self.row, column=7, pady=2)

        alt_subtitle_entry = Entry(feild_frame)
        alt_subtitle_entry.grid(row=self.row, column=8, pady=2)

        savedest_button = Button(feild_frame, text='Save as...', command=self.savedest_wrapper(feild_frame))
        savedest_button.grid(row=self.row, column=9, pady=2)
        
        self.batch.add_timeseries()

    def clear_selection(self):
        for frame in self.field_entry_frame.winfo_children():
            dic = frame.__dict__
            status = dic['children']['!checkbutton'].var.get()
            if status == 1:
                for obj in frame.winfo_children():
                    dic = obj.__dict__
                    if '!entry' in dic['_name']:
                        obj.delete(0, 'end')
                    if '!label3' == dic['_name']:
                        obj.var.set('               (No files imported)               ')
                    if '!label' == dic['_name']:
                        groupid = obj.var.get()
                        groupid = int(groupid.split()[1]) - 1
                        self.batch.timeseries_batch[groupid] = Timeseries()
                    
    def delete_selection(self):
        self.deleted_groups = []
        groups = []
        # identify selected groups
        for frame in self.field_entry_frame.winfo_children():
            dic = frame.__dict__
            status = dic['children']['!checkbutton'].var.get()
            if status == 1:
                for obj in frame.winfo_children():
                    dic = obj.__dict__
                    if '!label' == dic['_name']:
                        groupid = obj.var.get()
                        groupid = groupid.split()[1]
                        groupid = int(groupid) - 1
                        groups.append(groupid)
                    obj.destroy()
                frame.destroy()
            else:
                continue
        # reassign group numbers
        i = 1
        for frame in self.field_entry_frame.winfo_children():
            for obj in frame.winfo_children():
                dic = obj.__dict__
                if '!label' == dic['_name']:
                    group_text = 'Group ' + str(i)
                    obj.var.set(group_text)
                    i += 1 
        # save recently deleted groups for undo button (coming later)
        i = 0
        for groupid in groups:
            if i == 0:
                x = self.batch.timeseries_batch.pop(groupid)
            else:
                groupid -= 1
                x = self.batch.timeseries_batch.pop(groupid)
            self.deleted_groups.append(x)
            i += 1

    def add_color(self):
        Entry(self.general_params_frame).grid(row=self.colorrow, column=self.column, pady=2, sticky=W)
        self.column = self.column + 1
        if self.column == 8:
            self.colorrow = self.colorrow + 1
            self.column = 2
    
    def save_batch(self):
        pass

    def run(self):
        # save titles, subtitles, save file paths to Batch object
        # should follow order: title, subtitle, filepath in self.group_entry_frame.winfo_children() 
        for frame in self.field_entry_frame.winfo_children():
            i = 0
            for field in frame.winfo_children():
                dic = field.__dict__
                if dic['_name'] == '!label':
                    groupid = field.var.get()
                    groupid = groupid.split()[1]
                    groupid = int(groupid) - 1
                if '!entry' in dic['_name']:
                    entry = field.get()
                    if i == 0:
                        if entry == '':
                            continue
                        else:
                            self.batch.timeseries_batch[groupid].title = entry
                    if i == 1:
                        if entry == '':
                            continue
                        else:
                            self.batch.timeseries_batch[groupid].subtitle = entry
                    i += 1
            # if '!label3' == dic['_name']
        # save batch params related to x axis
        i = 0
        for item in self.x_ax_params_frame.winfo_children():
            dic = item.__dict__
            if '!entry' in dic['_name']:
                entry = item.get()
                if i == 0: # xmin
                    if entry == '':
                        self.batch.xmin = None
                    else:
                        self.batch.xmin = float(entry)
                if i == 1: # xmax
                    if entry == '':
                        self.batch.xmax = None
                    else:
                        self.batch.xmax = float(entry)
                if i == 2: # x major tick spacing
                    if entry == '':
                        self.batch.majorxticks = None
                    else:
                        self.batch.majorxticks = entry
                if i == 3: # x minor tick spacing
                    if entry == '':
                        self.batch.minorxticks = None
                    else:
                        self.batch.minorxticks = entry
                if i == 4: # x tick label font size
                    if entry == '':
                        self.batch.xtick_font_size = 13
                    else:
                        self.batch.xtick_font_size = float(entry)
                if i == 5: # x ax label
                    if entry == '':
                        self.batch.xlabel = None
                    else:
                        self.batch.xlabel = entry
                if i == 6: # x ax label font size
                    if entry == '':
                        self.batch.xlabel_font_size = 15
                    else:
                        self.batch.xlabel_font_size = float(entry)
                i += 1
        # y params
        i = 0
        for item in self.y_ax_params_frame.winfo_children():
            dic = item.__dict__
            if '!entry' in dic['_name']:
                entry = item.get()
                if i == 0: # ymin
                    if entry == '':
                        self.batch.ymin = None
                    else:
                        self.batch.ymin = float(entry)
                if i == 1: # ymax
                    if entry == '':
                        self.batch.ymax = None
                    else:
                        self.batch.ymax = float(entry)
                if i == 2: # y major tick spacing
                    if entry == '':
                        self.batch.majoryticks = None
                    else:
                        self.batch.majoryticks = entry
                if i == 3: # y minor tick spacing
                    if entry == '':
                        self.batch.minoryticks = None
                    else:
                        self.batch.minoryticks = entry
                if i == 4: # y tick label font size
                    if entry == '':
                        self.batch.ytick_font_size = 13
                    else:
                        self.batch.ytick_font_size = float(entry)
                if i == 5: # y ax label
                    if entry == '':
                        self.batch.ylabel = None
                    else:
                        self.batch.ylabel = entry
                if i == 6: # y ax label font size 
                    if entry == '':
                        self.batch.ylabel_font_size = 15
                    else:
                        self.batch.ylabel_font_size = float(entry)
                i += 1
        
        # get colors
        for item in self.general_params_frame.winfo_children():
            dic = item.__dict__
            if '!entry' in dic['_name']:
                if dic['_name'] != '!entry':
                    print(type(item))
                    entry = item.get()
                    self.batch.colors.append(entry)
            
        
        #get font
        self.batch.font = self.fontvar.get()
        
        # get timescale alterations
        if self.xscale_stringvar_actual.get() != self.xscale_stringvar.get():
            self.batch.alter_xscale = [self.xscale_stringvar_actual.get(), self.xscale_stringvar.get()]
        if self.yscale_stringvar_actual.get() != self.yscale_stringvar.get():
            self.alter_yscale = [self.yscale_stringvar_actual.get(), self.yscale_stringvar.get()]
        
        # get line width setting
        self.batch.linewidth = self.linewidth_var.get()

        # set secondary axis
        if self.top_var.get() == 0:
            self.batch.secondary_x = False
        else:
            self.batch.secondary_x = True
        
        if self.right_var.get() == 0:
            self.batch.secondary_y = False
        else:
            self.batch.secondary_y = True

        # set tick direction
        if self.direction_var.get() == 2:
            self.batch.direction = 'in'
        if self.direction_var.get() == 1:
            self.batch.direction = 'out'

        self.batch.run()


def main():
    root = App()
    root.mainloop()


if __name__ == '__main__':
    main()

