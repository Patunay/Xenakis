from tkinter import *
from tkinter import filedialog
from tkmacosx import Button
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import itertools

import config   # config module



prg_name= config.prg_name
pgr_ver=config.pgr_ver
# CONVERSION TO BACH ROLL MODULE

init_status = int() # 0 for modular, 1 for external

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
    # Populate path list
    def conv_set_params(self): # Rename!!! to somthing related to path list, not set anything
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
                thrs = 200
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
        if init_status == 1:
            normal_init()
        else:
            standalone_init()
        pass

    # Quit Program
    def kill(self):
        self.root.destroy()
        pass

    # Go to Generator program
    def mode_sel(self):
        self.root.destroy()
        starting_window_status = 1  #Open starting window
        pass 

    # PNG2Bach.Roll Algorithm
    def img_proc(self):
        bachroll_final = "" #String where all voices will be stored
        voiceadd_final = "" #String where all "insertvoice 1" will be stored
        counter = 1 #For voice number representation
        x = 0

        #Update input data with the one currently displayed in path_list
        filepaths = self.path_list.get(0, END)

        voices = len(filepaths)
        voiceloop = np.arange(voices)

        multiplier = int(self.lenght_entry.get())

        velocity = self.velocity_entry.get()    #Stays in string format
        
        threshold = int(self.threshold_entry.get())

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
            out = out.astype('float64')

            # Calculate range of inquiry
            inq = out[:,1]
            inq_max = max(inq)
            inq_min = min(inq)
            inq_range = inq_max - inq_min

            #Set output range 
            final_max = 10800       # To be later editable by user input
            final_min = 2100
            final_range = final_max - final_min

            out[:,1] = out[:,1] - inq_min 


            step_ = (final_range)/(inq_range)  

            out[:,1] = out[:,1] * step_
            out[:,1] = out[:,1] + 2100

            out[:,1] = 12900 - out[:,1] # invert mapping (math saves day yet again)

            out = np.rint(out)
            out = out.astype('int64')


            out[:,0] = out[:,0]*multiplier    #Handle Onsets and Durations
            out[:,2] = out[:,2]*multiplier

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
                s.append(velocity)                           #[ onset [ pitch duration velocity  
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
        self.show_output()
        pass
    pass

# Initialization modes definition for restart function
def normal_init():
    root = Tk()
    conv_window(root,config.prg_name +" "+ config.pgr_ver,config.pgr_ver)
    return None

def standalone_init():
    root = Tk()
    conv_window(root,config.prg_name +" "+ config.pgr_ver,config.pgr_ver + "~module")
    return None


# stuff to run always here such as class/def
def main():
    conv_window()
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   print("Standalone Launch")
   root = Tk()
   conv_window(root,prg_name +" "+ pgr_ver,pgr_ver)
   main()
