"""
################################################################################
################################################################################
################################################################################
Xenakis.app
    A graphic music notation translator
         by Carlos Mauro G.
            Feb, 2022
Ver Alpha 1.2
################################################################################
################################################################################
################################################################################
Notes on version Alpha 1.2:

This update achieved two main goals:
    -First working instance of GUI.
    -New functionalities:
        -Bach file selection.
        -File(voice) Order editor.
        -Display output as text:
            -Copy output to clipboard.
            -Optional "Save" option.
    -Enhaced comments.

In the next update:
    -Create and add function to "Reset" button to restart program.
    -Create individual voice preview option in frame 3.
    -Create gattered voice preview option in frame 3.
    -Implement Classes to organize code better.
    -Begin creating graphical editor.
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

'''
CODE
'''

from tkinter import *
from tkinter import filedialog
from tkmacosx import Button
from PIL import Image
import numpy as np
# import matplotlib.pyplot as plt  #For debuging only
import itertools


###Global Variables
voices = ""
voiceloop = []
multiplier = ""
velocity = ""
threshold = ""
filepaths = []
path_update = []
path_update_status = FALSE
result = ""


###############################
# START of FUNCTION DECLARATION
###############################


#Save as text file
def save():
    text_file = open("BachrollInput.txt", "w")  #Ask for specify name and path!!!
    text_file.write(result)
    text_file.close()
    return

#Text Editor output
def clipboard():
    global result
    clip = Tk()
    clip.withdraw()
    clip.clipboard_clear()
    clip.clipboard_append(result)
    clip.destroy()

#Show Text Output
def show_widget():
    global result

    fifth_frame = LabelFrame(root,text ="5) Bach.Roll String",padx=3,pady=3) #pad inside frame
    fifth_frame.grid(row=2,column=0,rowspan=4,padx=10,pady=10)   #pad outside

    entry11_button = Button(fifth_frame, text="Copy to Clipboard",bg="blue",fg="white",relief=RAISED,command=clipboard)   #Copy to Clipboard func
    entry11_button.grid(row=12,column=0)

    entry12_button = Button(fifth_frame, text="Save File",bg="blue",fg="white",relief=RAISED,command=save)   #Save File func
    entry12_button.grid(row=12,column=1)

    entry13_button = Button(fifth_frame, text="Reset",bg="orange",fg="white",relief=RAISED)   #Reset program func
    entry13_button.grid(row=12,column=2)

    quit_button = Button(fifth_frame, text="Quit",bg="red",fg="black",relief=RAISED,command=kill)    #Quit Program
    quit_button.grid(row=12,column=3)

    text_output = Text(fifth_frame,width=60,height=20)
    text_output.grid(row=13,column=0,columnspan=4)
    text_output.insert(END,result)   

#Quit Program
def kill():
    root.destroy()
    return

#Define function to hide the widget
def hide_widget(widget):
    widget.grid_forget()

#Set Params. Function
def click1():
    global voices
    global voiceloop
    global multiplier
    global velocity
    global threshold
    global filepaths

    voices = voice_entry.get()
    voices = int(voices)
    voiceloop = np.arange(voices) #Number of iterations needed excluding 1st pass

    multiplier = lenght_entry.get()
    multiplier = int(multiplier)

    velocity = velocity_entry.get()
    
    threshold = threshold_entry.get()
    threshold = int(threshold)

    filepaths = filedialog.askopenfilename(multiple=True)
    totalvoices = len(filepaths)
    filepaths = np.array_split(filepaths, totalvoices)
    display_paths()
    return

#Display Params. Function
def display_paths():
    global filepaths
    for path in filepaths:
        path_list.insert(END, path)
    return
    
#Change order of Paths
def path_move_up():
    global path_list
    text = path_list.get(ANCHOR)
    index = path_list.get(0, "end").index(text)
    if index == 0:
        path_list.delete(ANCHOR)
        path_list.insert("end", text)
        return
    path_list.delete(ANCHOR)
    path_list.insert(index-1, text)
    return

def path_move_down():
    global path_list
    text = path_list.get(ANCHOR)
    index = path_list.get(0, "end").index(text)
    path_list.delete(ANCHOR)
    path_list.insert(index+1, text)
    return

#Update Filepaths with new Order
def update_filepaths():
    global path_update
    global path_update_status
    path_update = path_list.get(0, END)
    path_update_status = TRUE

#PNG2Bach.Roll Algorithm
def img_proc():
    bachroll_final = "" #String where all voices will be stored
    voiceadd_final = "" #String where all "insertvoice 1" will be stored
    counter = 1 #For voice number representation
    global velocity
    global filepaths
    global threshold
    global result
    x = 0
    
    if path_update_status == TRUE:
        filepaths = path_update
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
        result = np.array(res)

        #Independization of events
        msr =  np.array(result.shape)   #To calculate i
        i = int(msr[0]/2)   #i = [result columns]/2 

        final = np.split(result, i) #Split into individual events

        end_array = np.arange(i)   #Iterator for upcoming loop

        subarray = 0   #Subarray number, it goes up every time until i ("end")

        comp = []   #Storage of durations of events
        for p in end_array:
            comp.append((final[subarray][1,1])-(final[subarray][0,1])+1) #get duration    (refers to specific objects in sub arrays)
            subarray += 1   #counter of sub array
        subarray = 0      #Resets counter to 0
        comp_array = np.array(comp)
        comp_array = comp_array[:,np.newaxis]

        out = result[::2]   #Gets starting onset and pitch
        out[:,[1,0]] = out[:,[0,1]]  #Swaps places of colums 

        out = np.concatenate((out,comp_array), axis=1)  #Sum everything
        out = out[np.lexsort(np.fliplr(out).T)]   #Ascending order///In Chronological Order

        out[:,1] = out[:,1]*(-50) + 11300    #Converted to midicents..!!

        out[:,0] = out[:,0]*multiplier    #Handle Onsets and Durations
        out[:,2] = out[:,2]*multiplier
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
    result = bachroll_final
    show_widget()
    return


###############################
# END of FUNCTION DECLARATION
###############################


'''
GUI
'''

#############################
# START of GUI for CONVERSION
#############################
root = Tk()
root.title("Xenakis ver. Alpha 1.2 ")

#Frames
big_frame = LabelFrame(root,padx=5,pady=5) #pad inside frame
big_frame.grid(row=0,column=0,padx=10,pady=10)   #pad outside

first_frame = LabelFrame(big_frame,text ="1) Set Parameters",padx=5,pady=5) #pad inside frame
first_frame.grid(row=1,column=0,columnspan=2,rowspan=4,padx=10,pady=10)   #pad outside

second_frame = LabelFrame(big_frame,text ="2) Select Files",padx=5,pady=5) #pad inside frame
second_frame.grid(row=5,column=0,columnspan=2,padx=10,pady=10)   #pad outside

third_frame = LabelFrame(big_frame,text ="3) Check Voice Order",padx=3,pady=3) #pad inside frame
third_frame.grid(row=1,column=2,rowspan=3,padx=10,pady=10)   #pad outside

fourth_frame = LabelFrame(big_frame,text ="4) Start",padx=3,pady=3) #pad inside frame
fourth_frame.grid(row=5,column=2,rowspan=4,padx=10,pady=10)   #pad outside

title_label = Label(big_frame, text="Xenakis",anchor=CENTER,font="helvetica 18 bold")
title_label.grid(row=0,column=0,columnspan=3)

#Labels corresponding entry fields
voices_label = Label(first_frame, text="Number of Voices")
voices_label.grid(row=1,column=0)

voice_entry = Entry(first_frame, width=3, borderwidth=2)
voice_entry.grid(row=1,column=1)
#
lenght_label = Label(first_frame, text="Lenght Multiplier")
lenght_label.grid(row=2,column=0)

lenght_entry = Entry(first_frame, width=3, borderwidth=2)
lenght_entry.grid(row=2,column=1)
#
velocity_label = Label(first_frame, text="MIDI Velocity")
velocity_label.grid(row=3,column=0)

velocity_entry = Entry(first_frame, width=3, borderwidth=2)
velocity_entry.grid(row=3,column=1)
#
threshold_label = Label(first_frame, text="Threshold")
threshold_label.grid(row=4,column=0)

threshold_entry = Entry(first_frame, width=3, borderwidth=2)
threshold_entry.grid(row=4,column=1)
#
filepath_label = Label(second_frame, text="Filepaths")
filepath_label.grid(row=0,column=0)

entry5_button = Button(second_frame, text="Open",bg="blue",fg="white",relief=RAISED,command=click1)
entry5_button.grid(row=0,column=1)
#
carlos_label = Label(big_frame, text="by Carlos Mauro G.",font="helvetica 10 italic")
carlos_label.grid(row=6,column=2)

#Preset Loader
preset = 1
if preset == 1:
    lenght_entry.insert(END,"250")
    velocity_entry.insert(END,"100")
    threshold_entry.insert(END,"200")

#Path List Display and Organization
path_list = Listbox(third_frame,height=7,width=30)
path_list.grid(row=0,column=0,columnspan=4)

entry6_button = Button(third_frame, text="Move Up",bg="blue",fg="white",relief=RAISED,command=path_move_up)
entry6_button.grid(row=1,column=0)

entry7_button = Button(third_frame, text="Move Down",bg="blue",fg="white",relief=RAISED,command=path_move_down)
entry7_button.grid(row=1,column=1)

entry8_button = Button(third_frame, text="Update Filepaths",bg="blue",fg="white",relief=RAISED,command=update_filepaths)
entry8_button.grid(row=1,column=2)

entry9_button = Button(fourth_frame, text="Start",bg="green",fg="black",relief=RAISED,command=img_proc)
entry9_button.grid(row=0,column=0)


###########################
# END of GUI for CONVERSION
###########################


###################################
# START of GUI for GRAPHICAL EDITOR
###################################





#New Window for editor


# def openNewWindow():
#     # Toplevel object which will
#     # be treated as a new window
#     newWindow = Toplevel(root)
 
#     # sets the title of the
#     # Toplevel widget
#     newWindow.title("Text Outout")
 
#     # sets the geometry of toplevel
#     newWindow.geometry("200x200")
 
#     # A Label widget to show in toplevel
#     Label(newWindow,
#           text ="This is a new window").pack()
 

# entry10_button = Button(root, text="New window",bg="red",fg="black",relief=RAISED,command=openNewWindow)
# entry10_button.grid(row=10,column=0)

# label = Label(root, text ="This is the main window")    #New window???
#########################


# text_file = open("BachrollInput.txt", "w")  #Create Text File
# text_file.write(bachroll_final)
# text_file.close()


#For debugin
# plt.imshow(img_bin, cmap="gray")
# plt.show()
root.mainloop()