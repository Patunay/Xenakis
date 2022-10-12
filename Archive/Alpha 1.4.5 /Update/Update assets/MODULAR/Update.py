from tkinter import *
from tkinter import filedialog
from tkmacosx import Button
from PIL import Image, ImageTk, ImageGrab
import matplotlib.pyplot as plt
import numpy as np
import itertools

import config
import starting_point
import algorithm



# General program information    # To be used in window naming and others...
prg_name= config.prg_name
pgr_ver=config.pgr_ver

# Class that contains Welcome window

# Class that contains Score Generation window

# Class for Graphical Editor window
class graph_editor:
    ##############################
    # CLASS VARIABLE DECLARATION #
    ##############################
       
    current_x, current_y = 0 ,0   # Mouse click tracker variable initialize
    draw_mode = 0                 # 0=no draw, 1=freehand, 2=assisted
    bound_show_state = 1          # To show bound grid

    ##############
    # CLASS INIT #
    ##############
    def __init__(self,root,title,version):
        self.root = root
        self.root.title(version)
        self.root.attributes('-fullscreen', True)

        #Frames
        self.topbar_frame = Frame(self.root, bd=1, relief="sunken")
        self.canvas_frame = Frame(self.root, bd=1, relief="sunken")
        self.botbar_frame = Frame(self.root, bd=1, relief="sunken")
        self.leftbar_frame = Frame(self.root, bd=1, relief="sunken")

        self.topbar_frame.grid(row=0, column=0,columnspan=2, sticky="nsew", padx=2, pady=2)
        self.canvas_frame.grid(row=1, column=1,columnspan=2, sticky="nsew", padx=2, pady=2)
        self.botbar_frame.grid(row=2, column=0,columnspan=2, sticky="nsew", padx=2, pady=2)
        self.leftbar_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        #Frame weights (how much space does it need)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=0)

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=3)

        #Labels on topbar_frame
        self.title_label = Label(self.topbar_frame, text = "Graphical Editor",font="helvetica 18 bold")
        self.title_label.grid(row=0,column=0,sticky="w")

        self.save_button = Button(self.topbar_frame, text="Save",bg="blue",fg="black",relief=RAISED,command= self.save_canvas)
        self.save_button.grid(row=0,column=1)

        self.load_button = Button(self.topbar_frame, text="Load",bg="blue",fg="black",relief=RAISED)
        self.load_button.grid(row=0,column=2)

        self.no_draw_button = Button(self.topbar_frame, text="No Draw",bg="blue",fg="black",relief=RAISED,command= lambda: self.draw_mode_sel(0))
        self.no_draw_button.grid(row=0,column=3)

        self.freehand_button = Button(self.topbar_frame, text="Freehand",bg="blue",fg="black",relief=RAISED,command= lambda: self.draw_mode_sel(1))
        self.freehand_button.grid(row=0,column=4)

        self.assisted_button = Button(self.topbar_frame, text="Assisted",bg="blue",fg="black",relief=RAISED,command= lambda: self.draw_mode_sel(2))        
        self.assisted_button.grid(row=0,column=5)

        self.new_layer_button = Button(self.topbar_frame, text="New Layer",bg="blue",fg="black",relief=RAISED)
        self.new_layer_button.grid(row=0,column=6)

        self.layers_button = Button(self.topbar_frame, text="Layers",bg="blue",fg="black",relief=RAISED)
        self.layers_button.grid(row=0,column=7)

        # Labels on leftbar_frame
        self.show_bound_button = Button(self.leftbar_frame, text="Bounds",bg="green",fg="black",relief=RAISED,command=self.show_hide_boundary) #commnad
        self.show_bound_button.grid(row=0,column=0)        

        ####INFINATE CANVAS KEY VARIABLE!!!! scrollregion=(0,0,x,0)  increment x as needed-implement botton that adds 1000 for every activation
        self.main_canvas = Canvas(self.canvas_frame,bg="white",scrollregion=(0,0,10000,900))
        self.main_canvas.pack(fill=BOTH, expand=True)

        hbar=Scrollbar(self.canvas_frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.main_canvas.xview)
        self.main_canvas.config(xscrollcommand=hbar.set)

        #Track mouse possition on Click! (Button 1)
        self.main_canvas.bind("<Button-1>", self.locate_xy)

        #Track mouse possition on Drag! (Button 1)
        self.main_canvas.bind("<B2-Motion>", self.addline)

        #Labels on botbar_frame
        self.home_button = Button(self.botbar_frame, text="Return to mode selection",bg="yellow",fg="black",relief=RAISED,command=self.go_home)
        self.home_button.grid(row=0,column=0,sticky="w")

        self.root.mainloop()
        pass
   
    ######################
    # METHOD DECLARATION #
    ######################

    #### Drawing modes
    # Draw Mode Handler    
    def draw_mode_sel(self,mode):   #Redundant? Double check later
        self.draw_mode = mode

    # Mouse coordenates generator on click
    def locate_xy(self,event):
        if self.draw_mode == 0: #No Draw Mode
            return
        if self.draw_mode in (1,2): #Freehand and Assisted mode share code
            self.main_canvas = event.widget
            x = self.main_canvas.canvasx(event.x)
            y = self.main_canvas.canvasy(event.y)
            self.current_x, self.current_y = x, y
            return
        pass
               
    # Mouse Drag
    def addline(self,event):
        if self.draw_mode == 0: #No Draw mode
            return
        if self.draw_mode == 1: #Freehand mode
            self.main_canvas = event.widget
            x = self.main_canvas.canvasx(event.x)
            y = self.main_canvas.canvasy(event.y)
            self.main_canvas.create_line(self.current_x, self.current_y,x,y)
            self.current_x, self.current_y = x,y
            return
        if self.draw_mode == 2: #Assisted mode
            self.main_canvas = event.widget
            x = self.main_canvas.canvasx(event.x)
            y = self.main_canvas.canvasy(event.y)
            self.main_canvas.create_line(self.current_x, self.current_y,x,y)
            return
        pass     

    ### General methods
    # Grid show/Hide 
    def show_hide_boundary(self): 
        if self.bound_show_state == 11: #Resets counter, keeps it between 1-10
            self.bound_show_state = 1
        if self.bound_show_state % 2 != 0:  #impar
            self.main_canvas.create_line(30,0,30,900,fill="red",tags="bound") #Tags to keep objects in track
            self.main_canvas.create_line(0,20,10000,20,fill="red",tags="bound")
            self.main_canvas.create_line(0,740,10000,740,fill="red",tags="bound")
            self.bound_show_state += 1
            return
        if self.bound_show_state % 2 == 0:  #par
            self.main_canvas.delete("bound")
            self.bound_show_state += 1
        return          
   
   # Save as .png
    def save_canvas(self):
        name = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if name is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        # save postscipt image 
        self.main_canvas.postscript(file = name + '.eps') 
        # use PIL to convert to PNG 
        img = Image.open(name + '.eps') 
        img.save(name + '.png', 'png')         
        pass

    #Go to Generator program
    def go_home(self):
        self.root.destroy()
        starting_point()
        pass 



# Invocation of Classes
def welcome():
    root = Tk()
    starting_point.welcome_window(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

def generate():
    # # config.algorithm_window_status = 1
    # if config.algorithm_window_status == 1:
    #     config.algorithm_window_status = 0
    root = Tk()
    algorithm.conv_window(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

def editor():
    root = Tk()
    graph_editor(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None
# 
#


# Define transitions between classes

#Go to Score Generator program
def start_generator():
    if config.algorithm_window_status == 1:
        generate()
    pass    


print("algorithm show status is ",config.algorithm_window_status)




# Initial state of program

welcome()

