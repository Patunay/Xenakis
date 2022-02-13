from tkinter import *
from tkinter import filedialog
from tkmacosx import Button
from PIL import Image, ImageTk, ImageGrab
import matplotlib.pyplot as plt
import numpy as np
import itertools

# General program information    # To be used in window naming and others...
prg_name= "Xenakis"
pgr_ver="Alpha 1.5"

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
    preview_status = 1
    result = ""

    ##############
    # CLASS INIT #
    ##############
    def __init__(self,root,title,version):
        self.root=root
        self.root.title(version)

        #Frames
        self.parent_frame = Frame(self.root, bd=1, relief="sunken")
        self.sec_frame = Frame(self.parent_frame, bd=1, relief="sunken")
        self.input_frame = LabelFrame(self.sec_frame, bd=1, relief="sunken",text="1) Set Parameters")
        self.filepath_frame = LabelFrame(self.sec_frame, bd=1, relief="sunken",text="3) Check voice order")
        self.options_frame = Frame(self.input_frame, bd=1, relief="sunken")
        self.filepath_set_frame = LabelFrame(self.input_frame, bd=1, relief="sunken",text="2) Select all files")
        self.filepath_list_frame = Frame(self.filepath_frame, bd=1, relief="sunken")
        self.filepath_options_frame = Frame(self.filepath_frame, bd=1, relief="sunken")

        self.parent_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.sec_frame.grid(row=1, column=0,columnspan=8, sticky="nsew", padx=2, pady=2)
        self.input_frame.grid(row=0, column=0,rowspan=5, sticky="nsew", padx=2, pady=2)
        self.filepath_frame.grid(row=0, column=2,columnspan=6, sticky="nsew", padx=2, pady=2)
        self.options_frame.grid(row=0, column=0,rowspan=4, sticky="nsew", padx=2, pady=10)
        self.filepath_set_frame.grid(row=4, column=0,columnspan=2, sticky="nsew", padx=2, pady=10)
        self.filepath_list_frame.grid(row=0, column=0,columnspan=5, sticky="nsew", padx=2, pady=2)
        self.filepath_options_frame.grid(row=1, column=0,columnspan=5, sticky="nsew", padx=2, pady=2)

        # Frame weights (how much space does it need)

        # In root:
        self.root.rowconfigure(0, weight=3)
        self.root.columnconfigure(0, weight=3)

        # In sec_frame:
        self.sec_frame.rowconfigure(0, weight=0)
        self.sec_frame.rowconfigure(1, weight=0)

        # for input_frame
        self.input_frame.columnconfigure(0, weight=0)
        self.input_frame.columnconfigure(1, weight=0)

        # for filepath_ frame
        self.sec_frame.columnconfigure(1, weight=3)

        # In filepath_frame
        self.filepath_frame.rowconfigure(0, weight=3)
        self.filepath_frame.columnconfigure(0, weight=3)

        self.filepath_frame.rowconfigure(1, weight=3)

        self.filepath_frame.columnconfigure(1, weight=3) 

        # In options_frame   
        self.options_frame.rowconfigure(0, weight=0)
        self.options_frame.rowconfigure(1, weight=0)
        self.options_frame.rowconfigure(2, weight=0)
        self.options_frame.rowconfigure(3, weight=0)  

        # In filepath_set
        self.filepath_set_frame.rowconfigure(0, weight=0)
        self.filepath_set_frame.columnconfigure(0, weight=0)

        # In filepath_list_frame
        self.filepath_list_frame.rowconfigure(0, weight=3)
        self.filepath_list_frame.columnconfigure(0, weight=3)

        # In filepath_options_frame
        self.filepath_options_frame.rowconfigure(0, weight=3)
        self.filepath_options_frame.columnconfigure(0, weight=0)

        # Widgets

        # Widgets on self.root
        self.entry10_button = Button(self.root, text="Return to mode selection",bg="yellow",fg="black",relief=RAISED,command=self.mode_sel)
        self.entry10_button.grid(row=5,column=0,sticky="w")
        #
        self.carlos_label = Label(self.root, text="Program developed by Carlos Mauro G.",font="helvetica 10 italic")
        self.carlos_label.grid(row=5,column=0,sticky="e")

        # Wiggets on parent_frame
        self.entry9_button = Button(self.parent_frame, text="Start",bg="green",fg="black",relief=RAISED,command=self.img_proc)
        self.entry9_button.grid(row=2,column=0,columnspan=8)
        #
        self.title_label = Label(self.parent_frame, text=title,font="helvetica 18 bold")
        self.title_label.grid(row=0,column=0,columnspan=8)

        # Widgets on options_frame
        # self.voices_label = Label(self.options_frame, text="Number of Voices:")
        # self.voices_label.grid(row=0,column=0,sticky="w")   

        # self.voice_entry = Entry(self.options_frame, width=3, borderwidth=2)
        # self.voice_entry.grid(row=0,column=1)
        #
        self.lenght_label = Label(self.options_frame, text="Lenght Multiplier:")
        self.lenght_label.grid(row=1,column=0,sticky="w")

        self.lenght_entry = Entry(self.options_frame, width=3, borderwidth=2)
        self.lenght_entry.grid(row=1,column=1)     
        #
        self.velocity_label = Label(self.options_frame, text="MIDI Velocity:")
        self.velocity_label.grid(row=2,column=0,sticky="w")

        self.velocity_entry = Entry(self.options_frame, width=3, borderwidth=2)
        self.velocity_entry.grid(row=2,column=1)      
        #
        self.threshold_label = Label(self.options_frame, text="Threshold:")
        self.threshold_label.grid(row=3,column=0,sticky="w")

        self.threshold_entry = Entry(self.options_frame, width=3, borderwidth=2)
        self.threshold_entry.grid(row=3,column=1)
        #          
        self.filepath_label = Label(self.filepath_set_frame, text="Filepaths:")
        self.filepath_label.grid(row=0,column=0,sticky="w")

        self.entry5_button = Button(self.filepath_set_frame,text="Open",bg="blue",fg="white",relief=RAISED,command= self.conv_set_params)
        self.entry5_button.grid(row=0,column=1,sticky="e")
        #

        # Widgets on filepath_list_frame
        self.path_list = Listbox(self.filepath_list_frame, selectmode=SINGLE)  
        self.path_list.grid(row=0,column=0,columnspan=5,sticky="nsew")
       
        #Widgets on filepath_frame
        self.entry6_button = Button(self.filepath_options_frame, text="Move Up",bg="blue",fg="white",relief=RAISED,command=self.path_move_up)
        self.entry6_button.grid(row=1,column=0)
        #
        self.entry7_button = Button(self.filepath_options_frame, text="Move Down",bg="blue",fg="white",relief=RAISED,command=self.path_move_down)
        self.entry7_button.grid(row=1,column=1)
        #
        self.entry11_button = Button(self.filepath_options_frame, text="Add Layer(s)",bg="blue",fg="white",relief=RAISED,command=self.add_path)
        self.entry11_button.grid(row=1,column=2)
        #
        self.entry12_button = Button(self.filepath_options_frame, text="Delete Layer",bg="blue",fg="white",relief=RAISED,command= self.delete_path) 
        self.entry12_button.grid(row=1,column=3)
        #
        self.entry8_button = Button(self.filepath_options_frame, text="Preview Combined",bg="blue",fg="white",relief=RAISED,command=self.preview_combined)
        self.entry8_button.grid(row=1,column=4)
        #

        #Preset Loader  -Eventually add multiple presets depending on file input or user preference
        preset = 1
        if preset == 1:
            self.lenght_entry.insert(END,"250")
            self.velocity_entry.insert(END,"100")
            self.threshold_entry.insert(END,"200")

        # Key binds
        self.path_list.bind("<space>", self.preview_voice)
        self.path_list.bind("a", self.preview_combined)


        self.root.mainloop()
        pass

    ######################
    # METHOD DECLARATION #
    ######################
    # Set Params. Function and display paths in list widget
    def conv_set_params(self):
        # self.multiplier = self.lenght_entry.get()
        # self.multiplier = int(self.multiplier)

        # self.velocity = self.velocity_entry.get()
        
        # self.threshold = self.threshold_entry.get()
        # self.threshold = int(self.threshold)

        self.filepaths = filedialog.askopenfilename(multiple=True)
        totalvoices = len(self.filepaths)
        self.filepaths = np.array_split(self.filepaths, totalvoices)

        for path in self.filepaths:  # Display paths in Path list
            self.path_list.insert(END, path)
        pass
    
    # Preview single voice
    def preview_voice(self,event=None):
        if self.preview_status == 11:
            self.preview_status = 1

        if self.preview_status % 2 !=0: #impar
            #Get path and format string
            path = self.path_list.get(ANCHOR)
            for r in (("[", ""), ("]", ""),("'", "")):  # File Path Formating>>>Eliminating multiple characters from string
                path = path.replace(*r)
            # get image
            image = ImageTk.PhotoImage(Image.open(path))
            # load image
            self.preview_status += 1
            self.panel_frame = Frame(self.filepath_frame, bd=1, relief="sunken")
            self.panel_frame.grid(row=0, column=7,rowspan=2, sticky="nsew", padx=2, pady=2)
            self.panel = Label(self.panel_frame, image=image)
            self.panel.image = image
            self.panel.grid(row=0,column=0)
            return
        if self.preview_status % 2 == 0:  #par
            self.preview_status += 1
            self.panel_frame.destroy()
            return
        pass

    def preview_combined(self,event=None):

        #Update input data with the one currently displayed in path_list
        filepaths = self.path_list.get(0, END)
        voices = len(filepaths)
        totalvoices = np.arange(voices)
        x = 0

        # Format filepaths
        filepathlist = []
        for total in totalvoices:
            filepath = filepaths[x]
            filepath = str(filepath)
            x += 1

            for r in (("[", ""), ("]", ""),("'", "")):  #File Path Formating>>>Eliminating multiple characters from string
                filepath = filepath.replace(*r)
            filepathlist.append(filepath)
        x = 0   # Resets counter just in case

        # Convert to binary
        data = []
        lenghts = []
        rows = []
        for filepath in filepathlist:
                org_img = np.array(Image.open(filepath))    #opening image of voice  
                blue = org_img[:,:,2]   #obtaining Blue values
                thrs = int(self.threshold_entry.get())
                binarized = 1.0 * (blue > thrs) # make all pixels 1 < threshold black  
                binarized = binarized.astype(int)
                data.append(binarized)

                lenghts.append(binarized.shape[1])  #Get sizes
                rows.append(binarized.shape[0])


        # Get maximun values
        col_max = max(lenghts)
        row_max = max(rows)


        # Normalize lenghts to maximun values
        fixedcols = []
        sub_counter = 0
        for x in data:
            inq_col = data[sub_counter].shape[1]
            inq_row = data[sub_counter].shape[0]
            if inq_col < col_max:
                newcolumns = col_max - inq_col
                added = np.ones((inq_row,newcolumns),dtype=int)
                fixed = np.append(data[sub_counter],added,axis=1)
                fixedcols.append(fixed)
            else:
                fixedcols.append(data[sub_counter])
            sub_counter += 1

        # Normalize columns to maximun values:
        fixedrows = []
        sub_counter = 0
        for x in fixedcols:
            inq_row = fixedcols[sub_counter].shape[0]
            fixed_col = fixedcols[sub_counter].shape[1]
            if inq_row < row_max:
                newrows = row_max - inq_row
                added = np.ones((newrows,fixed_col),dtype=int)
                fixed = np.append(fixedcols[sub_counter],added,axis=0)
                fixedrows.append(fixed)
            else:
                fixedrows.append(fixedcols[sub_counter])
            sub_counter += 1

        # ##########

        # Invert binary values
        inverted_binary = []
        sub_counter = 0
        for x in fixedrows:
            inv = fixedrows[sub_counter]^1
            sub_counter += 1 
            inverted_binary.append(inv)

        # Sum all 
        summed = []
        sub_counter = 0

        for x in inverted_binary:
            if sub_counter == 0:
                summed = np.array(x)
            else:
                summed = summed + x
            sub_counter += 1 

        summed = np.where(summed >= 1, 1, summed)
        summed = summed^1 

        plt.imsave('/Users/cmauro/Documents/Programs/Xenakis/Update/temp_file/temp_preview.png',summed,cmap="gray")   # save the array to .png 
        # Command to show!
        if self.preview_status == 11:
            self.preview_status = 1

        if self.preview_status % 2 !=0: #impar
            #Get path and format string
          
            image = ImageTk.PhotoImage(Image.open('/Users/cmauro/Documents/Programs/Xenakis/Update/temp_file/temp_preview.png'))
            # load image
            self.preview_status += 1
            self.panel_frame = Frame(self.filepath_frame, bd=1, relief="sunken")
            self.panel_frame.grid(row=0, column=7,rowspan=2, sticky="nsew", padx=2, pady=2)
            self.panel = Label(self.panel_frame, image=image)
            self.panel.image = image
            self.panel.grid(row=0,column=0)
            return
        if self.preview_status % 2 == 0:  #par
            self.preview_status += 1
            self.panel_frame.destroy()
            return
        pass

    # Filepath Managment
    def path_move_up(self):
        index = self.path_list.curselection() #Gets index of current selection
        index = index[0]  #   Converts tuple to int
        text = self.path_list.get(index)   #Gets filepath string
        if index == 0:  #If item is on index 0
            self.path_list.delete(index)
            self.path_list.insert("end", text)
            self.path_list.select_set("end")
            return
        self.path_list.delete(index)    #If item is not on index 0
        newindex = index - 1
        self.path_list.insert(newindex, text)
        self.path_list.select_set(newindex)
        pass
    def path_move_down(self):
        index = self.path_list.curselection() #Gets index of current selection
        index = index[0]  #   Converts tuple to int   
        text = self.path_list.get(index)   #Gets filepath string
        if index == len(self.path_list.get(0, END))-1:  #If index = max voices
            self.path_list.delete(index)
            self.path_list.insert(0, text)
            self.path_list.select_set(0)
            return
        self.path_list.delete(index)
        newindex = index + 1
        self.path_list.insert(newindex, text)
        self.path_list.select_set(newindex)
        pass

    def add_path(self): #Supports multiple paths at once
        new_paths = filedialog.askopenfilename(multiple=True)
        total_added = len(new_paths)
        new_paths = np.array_split(new_paths, total_added)
        for path in new_paths:  # Display paths in Path list
            self.path_list.insert(END, path)
        pass
    def delete_path(self):
        self.path_list.delete(ANCHOR)

    # Show Text Output
    def show_output(self):
        fifth_frame = LabelFrame(self.root,text ="Bach.Roll String",padx=3,pady=3) #pad inside frame
        fifth_frame.grid(row=1,column=0,rowspan=4,columnspan=2,padx=10,pady=10)   #pad outside

        self.entry11_button = Button(fifth_frame, text="Copy to Clipboard",bg="blue",fg="white",relief=RAISED,command=self.clipboard)   #Copy to Clipboard func
        self.entry11_button.grid(row=12,column=0)

        self.entry12_button = Button(fifth_frame, text="Save File",bg="blue",fg="white",relief=RAISED,command=self.save)   #Save File func
        self.entry12_button.grid(row=12,column=1)

        self.entry13_button = Button(fifth_frame, text="Reset",bg="orange",fg="white",relief=RAISED,command=self.restart)   #Reset program func
        self.entry13_button.grid(row=12,column=2)

        self.quit_button = Button(fifth_frame, text="Quit",bg="red",fg="black",relief=RAISED,command=self.kill)    #Quit Program
        self.quit_button.grid(row=12,column=3)

        self.text_output = Text(fifth_frame,width=108,height=20,bg="black",fg="green")
        self.text_output.grid(row=13,column=0,columnspan=4)
        self.text_output.insert(END,self.result) 
        pass

    # Save as text file
    def save(self):
        name = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if name is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        name.write(self.result)
        name.close()
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
        counter = 1 #For voice number representation in bach sintax
        x = 0

        #Update input data with the one currently displayed in path_list
        filepaths = self.path_list.get(0, END)
        voices = len(filepaths)
        voiceloop = np.arange(voices)
        multiplier = int(self.lenght_entry.get())
        velocity = self.velocity_entry.get()    #Stays in string format
        threshold = int(self.threshold_entry.get())
        raw_cumulative_out = np.array([[0,0,0,0]])

        lenghts = []

        ranges_for_clefs = [0]


        for total in voiceloop:
            filepath = filepaths[x]
            filepath = str(filepath)
            x += 1

            for r in (("[", ""), ("]", ""),("'", "")):  #File Path Formating>>>Eliminating multiple characters from string
                filepath = filepath.replace(*r)

            #Image to binary conversion
            org_img = np.array(Image.open(filepath))    #opening image of voice
            blue = org_img[:,:,2]   #obtaining Blue values
            thrs = threshold
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
            out = np.delete(out,[0,1], axis=0)  # Deletion of first guides (2 in total)

            flag = np.zeros((out.shape[0],1),dtype=int) # Create "HEY I START A NEW VOICE!!!" Flag

            flag[0,0] = 1   # Set first item to 1 "starting point of voice"
            flag[out.shape[0]-1,0] = -1   # Set last items to -1 to "]" in sintax

            out = np.append(out,flag,axis=1)

            raw_cumulative_out = np.append(raw_cumulative_out,out,axis=0)

            # Lenght of voice
            lenght = len(raw_cumulative_out)
            print(lenght)
            lenghts.append(lenght)
        print (lenghts)
        lenghts = np.array(lenghts)

        slice_indexes = lenghts - 1
        print(slice_indexes)
        # slice_indexes[0] = slice_indexes[0] - 1 # Account for 0s intialialization
        print(slice_indexes)
        ###########


        raw_cumulative_out = np.delete(raw_cumulative_out,[0],axis=0)  # Delete init zerosss

        # Mapping to Musical Register

        raw_cumulative_out = raw_cumulative_out.astype('float64')
        # Calculate range of inquiry
        inq = raw_cumulative_out[:,1]
        inq_max = max(inq)
        inq_min = min(inq)
        inq_range = inq_max - inq_min

        #Set output range 
        final_max = 10800       # To be later editable by user input
        final_min = 2100
        final_range = final_max - final_min

        raw_cumulative_out[:,1] = raw_cumulative_out[:,1] - inq_min 

        step_ = (final_range)/(inq_range)

        raw_cumulative_out[:,1] = raw_cumulative_out[:,1] * step_
        raw_cumulative_out[:,1] = raw_cumulative_out[:,1] + 2100

        raw_cumulative_out[:,1] = 12900 - raw_cumulative_out[:,1] # invert mapping (math saves day yet again)

        raw_cumulative_out = np.rint(raw_cumulative_out)
        raw_cumulative_out = raw_cumulative_out.astype('int64')


        raw_cumulative_out[:,0] = raw_cumulative_out[:,0]*multiplier    #Handle Onsets and Durations
        raw_cumulative_out[:,2] = raw_cumulative_out[:,2]*multiplier

        print("raw_cumul_out  shape is", raw_cumulative_out.shape)
        print(raw_cumulative_out)

        # Calculate clefs

        separated_voices = np.split(raw_cumulative_out,slice_indexes)   
        print(separated_voices)

        print(separated_voices[0])
        print(separated_voices[1])
        print(separated_voices[2])
        print(separated_voices[3])

        print()
        print(np.average(separated_voices[0],axis=0))

        print(separated_voices[0].shape) 
        af = separated_voices[0].shape
        af = af[1]

        clefloop = np.arange(af)     

        averages=[]
        cnt = 0
        for voices in clefloop:
            b = separated_voices[cnt][:, 1]                         # data of the cols
            print (b)
            avr = np.average(b)                    # average
            print(avr)
            averages.append(avr)
            cnt += 1
            pass

        print(averages) # Works
        # Now approximate 
        # Consider different ways of analizing data, study stadistics
        # Consider smart ordering







        # Convert to Bach.Roll Sintax

        sintax = np.split(raw_cumulative_out,raw_cumulative_out.shape[0])
        out_total_events = raw_cumulative_out.shape[0]
        out_total_events = np.arange(out_total_events)


        s = []
        for q in out_total_events:

            if sintax[subarray][0,3] == 1:
                counter = str(counter)
                s.append("addchords[" + counter)
                counter = int(counter)
                counter += 1

            s.append("[")                                #[
            s.append(sintax[subarray][0,0])              #[ onset
            s.append("[")                                #[ onset [
            s.append(sintax[subarray][0,1])              #[ onset [ pitch
            s.append(" ")                                # space
            s.append(sintax[subarray][0,2])              #[ onset [ pitch duration
            s.append(" ")                                # space
            s.append(velocity)                           #[ onset [ pitch duration velocity  
            s.append("]]")                               #[ onset [ pitch duration velocity]]

            if sintax[subarray][0,3] == -1:              # ]  "Final braket for voice"
                s.append("]")
            subarray += 1                                #go to next sub-array

        counter = 0   #Resets counter
        subarray = 0  #Resets subarray to 0
        string = "".join(map(str, s))       #Join Everything

        header = "insert voice 1,"*voices   # Creates nessesary headers


        bachroll = header + string    #finalized syntax out

        self.result = bachroll
        self.show_output()
        pass
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
def starting_point():
    root = Tk()
    welcome_window(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

def generate():
    root = Tk()
    conv_window(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

def editor():
    root = Tk()
    graph_editor(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

# Initial state of program
starting_point()