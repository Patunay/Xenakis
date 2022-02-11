"""
################################################################################
################################################################################
################################################################################
Xenakis.app
    A graphic music notation handler
         by Carlos Mauro G.
            Feb, 2022
Ver Alpha 1.3
################################################################################
################################################################################
################################################################################
Notes on version Alpha 1.3:
    This update achieved:
        -Creation of home-screen (starting point):
            -It shows and takes users to the functionalities of the program.
        -Implementation of the first instance of Graphical Editor
            -Fullscreen.
            -Supports multiple edit modes(drawing modes):
                -No Edit.
                -Freehand.
                -Assisted.
            -Scrollable (finite for now).
            -Function to Show/Hide Grid using tags.
            -Overall clean organization using frames and weights
        -Improvement of the Score Generation class.
            -Preview individual layers.
            -Improvement on visual design.
            -Reset botton working.
        -For all functionalities:
            -Botton to go back and forward between functionalities.
        -Organization of code using classes.
        -Enhanced comments.
        
    In the next update:
        -Score Generation:
            -Add customisation to SAVE AS!! [Name],[path selection]
            -Create gattered voice preview option in frame 3.
        -Graphic Editor:
            -Figure out:
                -Infinite Canvas
                -Layers
            -Improve Drawing modes
            -Save as local project
            -Export to .png
            -Direct generation of bach.roll.
            -Octave grids with Labels.
        -Figure out an elegant way to give credit to myself.

    Eventually:
        -Overhaul colors on GUI.
        -Realtime connection between graphical editor and Max Msp Software.


On Concepts Ipad app:
    Things to work on:
        -Create guides for diferrent intervals( 8ves done)
        -Create assets for different intervals
        -Togable (See only what you want to see)

    Eventually:
        -Figure out a format or create one yourself that allows you to embed all individual layers (voices) of a file in a single one.
        -add support for note velocity control on empty space abvove or below, maybe even use colors since its fairly easy to completely hide them.
        -Try creating files in illustrator
        -Create texture generators using np.arrays!!
        -Experiment with harmony
        -Create AI(??) to detect time information in score and expand lenght dynamically
################################################################################
################################################################################
################################################################################
"""

from tkinter import *
from tkinter import filedialog
from tkmacosx import Button
from PIL import Image, ImageTk
import numpy as np
import itertools

# General program information    # To be used in window naming and others...
prg_name= "Xenakis"
pgr_ver="Alpha 1.3"

# Class that contains Welcome window
class welcome_window:
    ##############
    # CLASS INIT #
    ##############
    def __init__(self,root,title,version):
        self.root = root
        self.root.title(version)

        #Grids
        welcome_frame = LabelFrame(self.root,padx=5,pady=5) #pad inside frame
        welcome_frame.grid(row=0,column=0,padx=10,pady=10)   #pad outside
        #secondary grid
        sec_frame = LabelFrame(welcome_frame,text="Select operation mode:",padx=5,pady=5) #pad inside frame
        sec_frame .grid(row=1,column=0,padx=10,pady=10)   #pad outside

        #Labels
        self.title_label = Label(welcome_frame, text = "Welcome to "+ title,font="helvetica 18 bold")
        self.title_label.grid(row=0,column=0)

        self.option1_label = Label(sec_frame, text = "Generate score")
        self.option1_label.grid(row=1,column=0,sticky="w")

        self.option2_label = Label(sec_frame, text = "Create score")
        self.option2_label.grid(row=2,column=0,sticky="w")

        self.option3_label = Label(sec_frame, text = "Edit score")
        self.option3_label.grid(row=3,column=0,sticky="w")

        self.carlos_label = Label(self.root, text="Program developed by Carlos Mauro G.",font="helvetica 10 italic")
        self.carlos_label.grid(row=1,column=0,sticky="e")

        #Buttons
        self.button1 = Button(sec_frame,width=37,bg="green",command=self.start_generator)
        self.button1.grid(row=1,column=1)

        self.button2 = Button(sec_frame,width=37,bg="green",command=self.start_graph)
        self.button2.grid(row=2,column=1)

        self.button3 = Button(sec_frame,width=37,bg="green")    #Place holder for new Class if needed
        self.button3.grid(row=3,column=1)

        self.root.mainloop()
        pass  

    ######################
    # METHOD DECLARATION #
    ######################

    #Go to Score Generator program
    def start_generator(self):
        self.root.destroy() # Destroy current
        generate()  #   Start new
        pass 

    #Go to Graph program
    def start_graph(self):
        self.root.destroy()
        editor()
        pass 

# Class that contains Score Generation window
class conv_window: 
    ##############################
    # CLASS VARIABLE DECLARATION #
    ##############################

    voices = ""
    voiceloop = []
    multiplier = ""
    velocity = ""
    threshold = ""
    filepaths = []
    path_update = []
    path_update_status = FALSE
    result = ""

    ##############
    # CLASS INIT #
    ##############
    def __init__(self,root,title,version):
        self.root=root
        self.root.title(version)

        #Frames
        self.big_frame = LabelFrame(self.root,padx=5,pady=5) #pad inside frame
        self.big_frame.grid(row=0,column=0,padx=10,pady=10,columnspan=2)   #pad outside

        first_frame = LabelFrame(self.big_frame,text ="1) Set Parameters",padx=5,pady=5) #pad inside frame
        first_frame.grid(row=1,column=0,columnspan=2,rowspan=4,padx=10,pady=10)   #pad outside

        second_frame = LabelFrame(self.big_frame,text ="2) Select Files",padx=5,pady=5) #pad inside frame
        second_frame.grid(row=5,column=0,columnspan=2,padx=10,pady=10)   #pad outside

        third_frame = LabelFrame(self.big_frame,text ="3) Check Voice Order",padx=3,pady=3) #pad inside frame
        third_frame.grid(row=1,column=2,rowspan=3,padx=10,pady=10)   #pad outside

        fourth_frame = LabelFrame(self.big_frame,text ="4) Start",padx=3,pady=3) #pad inside frame
        fourth_frame.grid(row=5,column=2,rowspan=4,padx=10,pady=10)   #pad outside

        title_label = Label(self.big_frame, text=title,anchor=CENTER,font="helvetica 18 bold")
        title_label.grid(row=0,column=0,columnspan=3)

        #Labels corresponding entry fields
        self.voices_label = Label(first_frame, text="Number of Voices")
        self.voices_label.grid(row=1,column=0,sticky="w")

        self.voice_entry = Entry(first_frame, width=3, borderwidth=2)
        self.voice_entry.grid(row=1,column=1)
        #
        self.lenght_label = Label(first_frame, text="Lenght Multiplier")
        self.lenght_label.grid(row=2,column=0,sticky="w")

        self.lenght_entry = Entry(first_frame, width=3, borderwidth=2)
        self.lenght_entry.grid(row=2,column=1)
        #
        self.velocity_label = Label(first_frame, text="MIDI Velocity")
        self.velocity_label.grid(row=3,column=0,sticky="w")

        self.velocity_entry = Entry(first_frame, width=3, borderwidth=2)
        self.velocity_entry.grid(row=3,column=1)
        #
        self.threshold_label = Label(first_frame, text="Threshold")
        self.threshold_label.grid(row=4,column=0,sticky="w")

        self.threshold_entry = Entry(first_frame, width=3, borderwidth=2)
        self.threshold_entry.grid(row=4,column=1)
        #
        self.filepath_label = Label(second_frame, text="Filepaths")
        self.filepath_label.grid(row=0,column=0,sticky="w")

        self.entry5_button = Button(second_frame, text="Open",bg="blue",fg="white",relief=RAISED,command= self.conv_set_params)
        self.entry5_button.grid(row=0,column=1)
        #
        self.carlos_label = Label(self.root, text="Program developed by Carlos Mauro G.",font="helvetica 10 italic")
        self.carlos_label.grid(row=20,column=1,sticky="e")

        #Preset Loader
        preset = 1
        if preset == 1:
            self.lenght_entry.insert(END,"250")
            self.velocity_entry.insert(END,"100")
            self.threshold_entry.insert(END,"200")

        #Path List Display and Organization
        self.path_list = Listbox(third_frame,height=7,width=68,selectmode=SINGLE)
        self.path_list.grid(row=0,column=0,columnspan=9)

        self.entry6_button = Button(third_frame, text="Move Up",bg="blue",fg="white",relief=RAISED,command=self.path_move_up)
        self.entry6_button.grid(row=1,column=0)

        self.entry7_button = Button(third_frame, text="Move Down",bg="blue",fg="white",relief=RAISED,command=self.path_move_down)
        self.entry7_button.grid(row=1,column=1)

        self.entry11_button = Button(third_frame, text="Preview Layer",bg="blue",fg="white",relief=RAISED,command=self.preview_voice)
        self.entry11_button.grid(row=1,column=2)

        self.entry12_button = Button(third_frame, text="EMPTY",bg="blue",fg="white",relief=RAISED) #####EMPTY
        self.entry12_button.grid(row=1,column=3)

        self.entry8_button = Button(third_frame, text="Update Order",bg="blue",fg="white",relief=RAISED,command=self.update_filepaths)
        self.entry8_button.grid(row=1,column=4)

        self.entry9_button = Button(fourth_frame, text="Start",bg="green",fg="black",relief=RAISED,command=self.img_proc)
        self.entry9_button.grid(row=0,column=0)

        self.entry10_button = Button(self.root, text="Return to mode selection",bg="yellow",fg="black",relief=RAISED,command=self.mode_sel)
        self.entry10_button.grid(row=20,column=0,sticky="w")

        self.root.mainloop()
        pass
    
    ######################
    # METHOD DECLARATION #
    ######################
    # Set Params. Function and display paths in list widget
    def conv_set_params(self):
        self.voices = self.voice_entry.get()
        self.voices = int(self.voices)
        self.voiceloop = np.arange(self.voices) # Number of iterations needed excluding 1st pass

        self.multiplier = self.lenght_entry.get()
        self.multiplier = int(self.multiplier)

        self.velocity = self.velocity_entry.get()
        
        self.threshold = self.threshold_entry.get()
        self.threshold = int(self.threshold)

        self.filepaths = filedialog.askopenfilename(multiple=True)
        totalvoices = len(self.filepaths)
        self.filepaths = np.array_split(self.filepaths, totalvoices)

        for path in self.filepaths:  # Display paths in Path list
            self.path_list.insert(END, path)
        pass
    
    # Preview single voice
    def preview_voice(self):
        #Get path and format string
        path = self.path_list.get(ANCHOR)
        print(path)
        for r in (("[", ""), ("]", ""),("'", "")):  # File Path Formating>>>Eliminating multiple characters from string
            path = path.replace(*r)
        # setup new window
        new_window = Toplevel(self.root)
        # get image
        image = ImageTk.PhotoImage(Image.open(path))
        # load image
        panel = Label(new_window, image=image)
        panel.image = image
        panel.pack()
        pass

    # Change order of Paths
    def path_move_up(self):
        text = self.path_list.get(ANCHOR)
        index = self.path_list.get(0, "end").index(text)
        if index == 0:
            self.path_list.delete(ANCHOR)
            self.path_list.insert("end", text)
            return
        self.path_list.delete(ANCHOR)
        newindex = index - 1
        self.path_list.insert(newindex, text)
        pass
    def path_move_down(self):
        text = self.path_list.get(ANCHOR)
        index = self.path_list.get(0, "end").index(text)
        self.path_list.delete(ANCHOR)
        newindex = index + 1
        self.path_list.insert(newindex, text)
        pass

    #Update Filepaths Order
    def update_filepaths(self):
        self.path_update = self.path_list.get(0, END)
        self.path_update_status = TRUE
        pass

    # Show Text Output
    def show_widget(self):
        fifth_frame = LabelFrame(self.root,text ="5) Bach.Roll String",padx=3,pady=3) #pad inside frame
        fifth_frame.grid(row=9,column=0,rowspan=4,columnspan=2,padx=10,pady=10)   #pad outside

        self.entry11_button = Button(fifth_frame, text="Copy to Clipboard",bg="blue",fg="white",relief=RAISED,command=self.clipboard)   #Copy to Clipboard func
        self.entry11_button.grid(row=12,column=0)

        self.entry12_button = Button(fifth_frame, text="Save File",bg="blue",fg="white",relief=RAISED,command=self.save)   #Save File func
        self.entry12_button.grid(row=12,column=1)

        self.entry13_button = Button(fifth_frame, text="Reset",bg="orange",fg="white",relief=RAISED,command=self.restart)   #Reset program func
        self.entry13_button.grid(row=12,column=2)

        self.quit_button = Button(fifth_frame, text="Quit",bg="red",fg="black",relief=RAISED,command=self.kill)    #Quit Program
        self.quit_button.grid(row=12,column=3)

        self.text_output = Text(fifth_frame,width=108,height=20)
        self.text_output.grid(row=13,column=0,columnspan=4)
        self.text_output.insert(END,self.result) 
        pass

    # Save as text file
    def save(self):
        text_file = open("BachrollInput.txt", "w")  # Ask for specify name and path!!!
        text_file.write(self.result)
        text_file.close()
        pass

    # Copy to clipboard
    def clipboard(self):
        clip = Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(self.result)
        clip.destroy()
        pass

    # Restart Program
    def restart(self):
        self.root.destroy()
        generate()
        pass

    # Quit Program
    def kill(self):
        self.root.destroy()
        pass

    # Go to Generator program
    def mode_sel(self):
        self.root.destroy()
        starting_point()
        pass 

    # PNG2Bach.Roll Algorithm
    def img_proc(self):
        bachroll_final = "" #String where all voices will be stored
        voiceadd_final = "" #String where all "insertvoice 1" will be stored
        counter = 1 #For voice number representation
        x = 0

        if self.path_update_status == TRUE:
            self.filepaths = self.path_update
        for total in self.voiceloop:
            filepath = self.filepaths[x]
            filepath = str(filepath)
            x += 1

            for r in (("[", ""), ("]", ""),("'", "")):  #File Path Formating>>>Eliminating multiple characters from string
                filepath = filepath.replace(*r)

            #Image to binary conversion
            org_img = np.array(Image.open(filepath))    #opening image of voice
            blue = org_img[:,:,2]   #obtaining Blue values
            thrs = self.threshold
            binarized = 1.0 * (blue > thrs) # make all pixels 1 < threshold black

            #Calculate lenght based on binary image
            res = []
            for rowIdx, row in enumerate(binarized):
                colIdx = 0                       #start column index
                for k, grp in itertools.groupby(row):
                    vals = list(grp)                   #Values in the group
                    lgth = len(vals)                  #Lenght of the group
                    colIdx2 = colIdx + lgth - 1       #end of column index

                    if k == 0 and lgth >= 2:           #Record this group if under threshhold
                        res.append([rowIdx,colIdx])
                        res.append([rowIdx, colIdx2])
                    colIdx = colIdx2 + 1              #Advance column index
            raw_list = np.array(res)

            #Independization of events
            msr =  np.array(raw_list.shape)   #To calculate i
            i = int(msr[0]/2)   #i = [result columns]/2 

            final = np.split(raw_list, i) #Split into individual events

            end_array = np.arange(i)   #Iterator for upcoming loop

            subarray = 0   #Subarray number, it goes up every time until i ("end")

            comp = []   #Storage of durations of events
            for p in end_array:
                comp.append((final[subarray][1,1])-(final[subarray][0,1])+1) #get duration    (refers to specific objects in sub arrays)
                subarray += 1   #counter of sub array
            subarray = 0      #Resets counter to 0
            comp_array = np.array(comp)
            comp_array = comp_array[:,np.newaxis]

            out = raw_list[::2]   #Gets starting onset and pitch
            out[:,[1,0]] = out[:,[0,1]]  #Swaps places of colums 

            out = np.concatenate((out,comp_array), axis=1)  #Sum everything
            out = out[np.lexsort(np.fliplr(out).T)]   #Ascending order///In Chronological Order

            out[:,1] = out[:,1]*(-50) + 11300    #Converted to midicents..!!

            out[:,0] = out[:,0]*self.multiplier    #Handle Onsets and Durations
            out[:,2] = out[:,2]*self.multiplier
            out = out.astype("int64")

            out = np.delete(out,[0,1], axis=0)  # Deletion of first guides (2 in total)
            end_array = np.delete(end_array,[0,1], axis=0)

            #########################Syntax creation    
            i_syntax = i - 2 #Adjust new i to the deletion of the 2 guides
            sintax = np.split(out, i_syntax)

            s = []
            for q in end_array:
                s.append("[")                                #[
                s.append(sintax[subarray][0,0])              #[ onset
                s.append("[")                                #[ onset [
                s.append(sintax[subarray][0,1])              #[ onset [ pitch
                s.append(" ")                                # space
                s.append(sintax[subarray][0,2])              #[ onset [ pitch duration
                s.append(" ")                                # space
                s.append(self.velocity)                           #[ onset [ pitch duration velocity  
                s.append("]]")                               #[ onset [ pitch duration velocity]]
                subarray += 1                                #go to next sub-array
            s.append("]")                                    #final "]"
            subarray = 0                        #Resets subarray to 0
            string = "".join(map(str, s))       #Join Everything

            counter = str(counter)
            pred = "addchords[" + counter
            counter = int(counter)
            counter += 1    #Counter goes up

            bachroll = pred + string    #finalized syntax out

            voiceadd_final = voiceadd_final + "insert voice 1,"
            bachroll_final = bachroll_final + bachroll

        bachroll_final = voiceadd_final + bachroll_final
        self.result = bachroll_final
        self.show_widget()
        pass

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

        self.save_button = Button(self.topbar_frame, text="Save",bg="blue",fg="black",relief=RAISED)
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
    def draw_mode_sel(self,mode):
        self.draw_mode = mode
        print("botton is working", mode)

        if self.draw_mode == 0:
            print("None")
        if self.draw_mode ==1:
            print("Free")
        if self.draw_mode ==2:  
            print("Assisted")

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
   
    #Go to Generator program
    def go_home(self):
        self.root.destroy()
        starting_point()
        pass 
        

# Invocation of Classes
def starting_point():
    root = Tk()
    window = welcome_window(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

def generate():
    root = Tk()
    window1 = conv_window(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

def editor():
    root = Tk()

    window2 = graph_editor(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

# Initial state of program
starting_point()