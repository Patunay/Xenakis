from tkinter import *
from tkinter import filedialog
from tkmacosx import Button
from PIL import Image, ImageTk, ImageGrab
import matplotlib.pyplot as plt
import numpy as np
import itertools
from datetime import date, datetime
import os


# General program information    # To be used in window naming and others...
prg_name= "Xenakis"
pgr_ver="Alpha 1.5"

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
        self.input_frame = LabelFrame(self.sec_frame, bd=1, relief="sunken",text="1) Set Parameters",font="helvetica")
        self.filepath_frame = LabelFrame(self.sec_frame, bd=1, relief="sunken",text="3) Check voice order",font="helvetica")
        self.options_frame = Frame(self.input_frame, bd=1, relief="sunken")
        self.filepath_set_frame = LabelFrame(self.input_frame, bd=1, relief="sunken",text="2) Select all files",font="helvetica")
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
        self.carlos_label = Label(self.root, text="Program developed by Carlos Mauro G.",font="helvetica 10 italic") #,bg=GUI_colors.color())
        self.carlos_label.grid(row=5,column=0,sticky="e")

        # Wiggets on parent_frame
        self.entry9_button = Button(self.parent_frame, text="Start",bg="#1494B8",fg="white",relief=RAISED,command=self.img_proc)
        self.entry9_button.grid(row=2,column=1,columnspan=1)

        self.lenght_inquiry = Button(self.parent_frame, text="How long?",relief=RAISED,command=self.verify_lenght)
        self.lenght_inquiry.grid(row=2,column=0,columnspan=1)


        #
        self.title_label = Label(self.parent_frame, text=title,font="helvetica 18 bold",fg="#22292B") # ,bg=GUI_colors.color())
        self.title_label.grid(row=0,column=0,columnspan=8)

        # Widgets on options_frame
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

        self.min_pitch_label = Label(self.options_frame,text="Min. Pitch:")
        self.min_pitch_label.grid(row=4,column=0,sticky="w")

        self.min_pitch_entry = Entry(self.options_frame, width=5, borderwidth=2)
        self.min_pitch_entry.grid(row=4,column=1)

        #

        self.max_pitch_label = Label(self.options_frame,text="Max. Pitch:")
        self.max_pitch_label.grid(row=5,column=0,sticky="w")

        self.max_pitch_entry = Entry(self.options_frame, width=5, borderwidth=2)
        self.max_pitch_entry.grid(row=5,column=1)

        #

        self.filepath_label = Label(self.filepath_set_frame, text="Filepaths:")
        self.filepath_label.grid(row=0,column=0,sticky="w")

        self.entry5_button = Button(self.filepath_set_frame,text="Open",bg="#1494B8",fg="white",relief=RAISED,command= self.conv_set_params)
        self.entry5_button.grid(row=0,column=1,sticky="e")
        #

        # Widgets on filepath_list_frame
        self.path_list = Listbox(self.filepath_list_frame, selectmode=SINGLE)  
        self.path_list.grid(row=0,column=0,columnspan=5,sticky="nsew")

        #Widgets on filepath_frame
        self.entry6_button = Button(self.filepath_options_frame, text="Move Up",bg="#016F8D",fg="white",relief=RAISED,command=self.path_move_up)
        self.entry6_button.grid(row=1,column=0)
        #
        self.entry7_button = Button(self.filepath_options_frame, text="Move Down",bg="#016F8D",fg="white",relief=RAISED,command=self.path_move_down)
        self.entry7_button.grid(row=1,column=1)
        #
        self.entry11_button = Button(self.filepath_options_frame, text="Add Layer(s)",bg="#016F8D",fg="white",relief=RAISED,command=self.add_path)
        self.entry11_button.grid(row=1,column=2)
        #
        self.entry12_button = Button(self.filepath_options_frame, text="Delete Layer",bg="#016F8D",fg="white",relief=RAISED,command= self.delete_path) 
        self.entry12_button.grid(row=1,column=3)
        #
        self.entry8_button = Button(self.filepath_options_frame, text="Preview Combined",bg="#016F8D",fg="purple",relief=RAISED,command=self.preview_combined)
        self.entry8_button.grid(row=1,column=4)
        #

        # Preset Loader  - Eventually add multiple presets depending on file input or user preference
        preset = 1
        if preset == 1:
            self.lenght_entry.insert(END,"250")
            self.velocity_entry.insert(END,"100")
            self.threshold_entry.insert(END,"200")
            self.min_pitch_entry.insert(END,"2100")
            self.max_pitch_entry.insert(END,"10800")

        # Key binds
        self.path_list.bind("<space>", self.preview_voice)
        self.path_list.bind("a", self.preview_combined)

        # Load formating config

        self.root.mainloop()
        pass

    ######################
    # METHOD DECLARATION #
    ######################

    def verify_lenght(self):

        # add estimated time here based on last event an multiplier
        #Update input data with the one currently displayed in path_list
        multiplier = int(self.lenght_entry.get())
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
        estimated_duration= (col_max * multiplier) /  60000

        minutes = int(estimated_duration)
        seconds = estimated_duration - minutes

        seconds = (seconds*60)
        seconds = np.rint(seconds)
        seconds = int(seconds)

        print(f"{minutes} min. : {seconds} sec.")
        pass

    # Set Params. Function and display paths in list widget
    def conv_set_params(self):
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

            # Command to show!
            global pop
            pop = Toplevel(self.root)
            pop.title("Individual Preview")

            # load and display image to new window
            img = Image.open(path)
            self.tkimage = ImageTk.PhotoImage(img)
            label = Label(pop, image=self.tkimage)
            label.pack()

        pass

    def preview_combined(self,event=None):

        # add estimated time here based on last event an multiplier
        # 
        #   
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

        plt.imsave('/Users/cmauro/Programs/Xenakis/Main/temp_img/temp_img.png',summed,cmap="gray")   # save the array to .png 

        # Command to show!
        global pop                          # Why global variable? 
        pop = Toplevel(self.root)
        pop.title("Combined Preview")

        # load and display image to new window
        img = Image.open('/Users/cmauro/Programs/Xenakis/Main/temp_img/temp_img.png')
        self.tkimage = ImageTk.PhotoImage(img)
        label = Label(pop, image=self.tkimage)
        label.pack()
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

    # Restart Program
    def restart(self):
        self.root.destroy()
        starting_point()
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

    def Create_Dir_Name(self):
        cur_day = str(date.today())
        time = datetime.now()
        hr, mn, s = time.hour, time.minute, time.second
        current_time = f"{hr}'{mn}''{s}'''"
        dir_name = cur_day + "_" + current_time
        return dir_name

    def create_dir(self,new_dir_path):
        os.makedirs(new_dir_path)
        return new_dir_path


    # PNG2Bach.Roll Algorithm
    def img_proc(self):

        # Update input data with the one currently displayed in path_list
        filepaths = self.path_list.get(0, END)
        voices = len(filepaths)
        voiceloop = np.arange(voices)
        multiplier = int(self.lenght_entry.get())
        velocity = self.velocity_entry.get()    #Stays in string format
        threshold = int(self.threshold_entry.get())
        fnl_mn = int(self.min_pitch_entry.get())
        fnl_mx = int(self.max_pitch_entry.get())

        def init_voices(total_voices):
            event_container = np.zeros(4, dtype=int)
            event_container= event_container[np.newaxis,:]
            init_zeros = np.array([[0,0,0,0]])

            for i in range(total_voices-1):
                event_container = np.append(init_zeros,event_container,axis=0)

            # Create individual subarrays for voice storage
            event_container = np.split(event_container,total_voices)
            return event_container


        def primary_proc():
            x = 0   # Counter for filepath formating
            subarray = 0   # Subarray number, ++ every time until i ("end")

            #Calculate lenght based on binary image
            def calculate_lenghts_from_binary(binarized_image_array):
                res = []
                for rowIdx, row in enumerate(binarized_image_array):
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
                return raw_list


            macro_container = init_voices(voices)


            for total in voiceloop:
                filepath = filepaths[x]
                filepath = str(filepath)

                for r in (("[", ""), ("]", ""),("'", "")):  #File Path Formating>>>Eliminating multiple characters from string
                    filepath = filepath.replace(*r)

                #Image to binary conversion
                org_img = np.array(Image.open(filepath))    #opening image of voice
                blue = org_img[:,:,2]   #obtaining Blue values
                thrs = threshold
                binarized = 1.0 * (blue > thrs) # make all pixels 1 < threshold black


                raw_list = calculate_lenghts_from_binary(binarized)


                #Independization of events
                msr =  np.array(raw_list.shape)   #To calculate i
                i = int(msr[0]/2)   # i = [result columns]/2 
                final = np.split(raw_list, i) #Split into individual events
                end_array = np.arange(i)   #Create iterator for upcoming loop


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

                flag = np.zeros((out.shape[0],1),dtype=int) # Create "HEY I START A NEW VOICE!!!" Flag

                flag[0,0] = 1   # Set first item to 1 "starting point of voice"
                flag[out.shape[0]-1,0] = -1   # Set last items to -1 to "]" in sintax

                out = np.append(out,flag,axis=1)
                # out = out.astype("float64")

                macro_container[x] = np.append(macro_container[x],out,axis=0) # add row to event_container
                macro_container[x] = np.delete(macro_container[x], [0], axis=0)
                x += 1

            return macro_container


        mapped_pitches_container = init_voices(voices)
        raw_cumul_out = primary_proc()

        def mapping_function(raw_cumul_out):
            x = 0
            local_min = []
            local_max = []
            for voice in raw_cumul_out:
                inq = voice[:,1]
                inq_max = max(inq)
                inq_min = min(inq)
                
                local_max.append(inq_max)
                local_min.append(inq_min)


            universal_max = max(local_max)
            universal_min = min(local_min)


            # Sets output range
            final_max = fnl_mx       
            final_min = fnl_mn

            for voice in raw_cumul_out: # Now compute mapping
                inq = voice[:,1]
                inq_max = universal_max
                inq_min = universal_min
                inq_range = inq_max - inq_min

                final_range = final_max - final_min

                voice[:,1] = voice[:,1] - inq_min 

                step_ = (final_range)/(inq_range)

                voice[:,1] = voice[:,1] * step_
                voice[:,1] = voice[:,1] + 2100

                voice[:,1] = 12900 - voice[:,1] # invert mapping (math saves day yet again)

                voice = np.rint(voice)    # Aproximate
                voice = voice.astype('int64')

                voice[:,0] = voice[:,0]*multiplier    #Handle Onsets and Durations
                voice[:,2] = voice[:,2]*multiplier

                mapped_pitches_container[x] = np.append(mapped_pitches_container[x],voice,axis=0) # add row to event_container
                mapped_pitches_container[x] = np.delete(mapped_pitches_container[x], [0], axis=0)
                x += 1

            return mapped_pitches_container

        mapped_data = mapping_function(raw_cumul_out)


        def calc_order_voices(data):
            cnt = 0 # For indexing subarrays in mapped data
            averages = []

            for i in data: 
                b = i[:, 1] # data of the cols
                avr = np.average(b)                    # average
                avr = (avr,cnt)
                averages.append(avr)
                cnt += 1
            cnt = 0


            # Now Reorder
            averages.sort(reverse=True)
            averages = np.array(averages)
            order = averages[:,1]
            order = order.astype("int64")


            # CREATE ORDERED CUMULATIVE LIST
            final_array = np.array([[0,0,0,0]])
            for index in order:
                events = data[index]          
                final_array = np.append(final_array,events,axis=0)
            final_array = np.delete(final_array,[0],axis=0)  # Delete init zerosss
            return final_array

        final_array = calc_order_voices(mapped_data)
        final_array[-1,3] = -2 # "END OF FILE" flag

        # Create .csv and organize output folder
        dir_name = self.Create_Dir_Name()
        directory_path = f"/Users/cmauro/Programs/Xenakis/Main/Output/{dir_name}"
        self.create_dir(directory_path)

        def csv_header_creator(total_voices, total_events, multiplier_factor):
            header = np.array([[-9,total_voices,total_events,multiplier_factor]], dtype=int)    # -9 is header flag
            return header

        csv_header = csv_header_creator(voices,final_array.shape[0],multiplier)
        print(csv_header)

        final_csv = np.append(csv_header,final_array,axis=0)

        np.savetxt(f"{directory_path}/{dir_name}.csv", final_csv, delimiter=",")

        # Convert to Bach.Roll Sintax
        counter = 0 # For voice number representation in bach sintax

        # Final event counter 
        sintax = np.split(final_array,final_array.shape[0]) # Divide into idividual events

        out_total_events = final_array.shape[0]
        out_total_events = np.arange(out_total_events)

        max_events_per_batch = 9999
        event_cntr = 0
        macro_sxyntax = []  # List of strings containing individual batches
        macro_conter = 0
        s = []  # Syntax container
        add_chord_flag = FALSE


        for event in sintax:    # por cada evento en el global container de eventos
            if event_cntr == max_events_per_batch:  # Force break to create batch
                print(macro_conter)
                print(event_cntr)
                if macro_conter != 0:   # if not first batch
                    if add_chord_flag == FALSE:
                        print("la cagaste, algo no funciona")
                        macro_conter += 1
                        s.append("]")
                        temp_syntx = "".join(map(str, s))       # Join Everything
                        temp_syntx = f"addchords[{str(counter)}" + temp_syntx
                        macro_sxyntax.append(temp_syntx)
                        add_chord_flag = TRUE

                        pass
                    else:
                        macro_conter += 1
                        s.append("]")
                        temp_syntx = "".join(map(str, s))       # Join Everything
                        macro_sxyntax.append(temp_syntx)
                        pass
                    s = []  # Reset string holder
                    event_cntr = 0  # Reset counter
                elif macro_conter == 0:   # if first batch
                    macro_conter += 1
                    s.append("]")
                    temp_syntx = "".join(map(str, s))       # Join Everything
                    macro_sxyntax.append(temp_syntx)    # Commit data to master container
                    s = []  # Reset string holder
                    s.append(f"")
                    event_cntr = 0  # Reset counter
                    # print("funciona hasta aca")

            # en caso de ser 1 sola voz, no reconoce el input de add chord si exede el maximo permitido


            if event[0,3] == 1:  # Start of voice
                counter += 1
                s.append(f"addchords[{str(counter)}")
                event_cntr += 1
                add_chord_flag = TRUE

            s.append("[")                                #[
            s.append(event[0,0])              #[ onset
            s.append("[")                                #[ onset [
            s.append(event[0,1])              #[ onset [ pitch
            s.append(" ")                                # space
            s.append(event[0,2])              #[ onset [ pitch duration
            s.append(" ")                                # space
            s.append(velocity)                           #[ onset [ pitch duration velocity  
            s.append("]]")                               #[ onset [ pitch duration velocity]]


            if event[0,3] == -1:              # ]  "Final braket for voice"
                s.append("]")

            if event[0,3] == -2:              # Commit to .txt if SMALL file
                s.append("]")
                temp_syntx = "".join(map(str, s))       # Join Everything
                macro_sxyntax.append(temp_syntx)
            event_cntr += 1


        # Create out folder
        file_path_prefix = f"{directory_path}/batch_"
        file_out_cntr = 1
        for i in macro_sxyntax: # Dynamic .txt file creator
            fname = f"{file_path_prefix}{file_out_cntr}.txt"
            with open(fname,"w+") as f:
                f.write(i)
            file_out_cntr += 1
        pass


# Invocation of Classes
def starting_point():
    root = Tk()
    conv_window(root,prg_name +" "+ pgr_ver,pgr_ver)
    return None

# Initial state of program
starting_point()