"""
################################################################################
Xenakis.app
    A graphic music notation translator
         by Carlos Mauro G.
            Feb, 2022
Ver Alpha 1.1
################################################################################
Notes on version Alpha 1.1:

This version achieved two main goals:
    -Make the code a lot more readable, mantainable, and expandable.
        --A main function was created instead of reusing code.
        --Revision of variable names.
        --Elimination of redundancies.
        --Enhanced comments.
    -Add options to adjust global parameters (threshold, velocity, lenght multiplier)


In the next update:
    -Add essential GUI to create a standalone application
    -Filepath selection helper
        --Make it a lot easier to import and organize layers using GUI

Things to work on: (On Concepts)
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
"""

from PIL import Image
import numpy as np
# import matplotlib.pyplot as plt  #For debuging only
import itertools

'''
Main Function
'''
#Composite Function (Img2Bachroll)

def img_proc():
    bachroll_final = "" #String where all voices will be stored
    voiceadd_final = "" #String where all "insertvoice 1" will be stored
    counter = 1 #For voice number representation
    global velocity
    for total in voiceloop:

        print ("Enter filepath of voice", counter)  #Selection of Voice
        filepath = input()

        #Image to binary conversion
        org_img = np.array(Image.open(filepath))    #opening image of voice
        blue = org_img[:,:,2]   #obtaining Blue values
        global threshold
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
    return bachroll_final
    
'''
Global Properties Setup
'''

voices = int(input("Enter number of voices "))  #Number of 3rd Dimensions
voiceloop = np.arange(voices) #Number of iterations needed excluding 1st pass

multiplier = 250 #Lenght Multiplier adjustments
multiplier_mod =input("Do you wish to enter custom lenght multiplier? 250 by default. (y/n) ")
if multiplier_mod == "y":
    multiplier_update = int(input("Enter new multiplier "))
    multiplier = multiplier_update

velocity = 100 #velocity adjustments
velocity_mod =input("Do you wish to enter a preffered MIDI velocity? 100 by default. (y/n) ")
if multiplier_mod == "y":
    velocity_update = int(input("Enter new velocity "))
    velocity = velocity_update

threshold = 200 #Threshhold for binary conversion adjustments
threshold_mod =input("Do you wish to alter greyscale converter threshold? 200 by default. (y/n) ")
if threshold_mod == "y":
    threshold_update = int(input("Enter new threshold "))
    threshold = threshold_update

'''
Main Function call
'''

result = img_proc() #Convert images to data (Starting & Ending points)

'''
Create text file
'''
text_file = open("BachrollInput.txt", "w")
text_file.write(result)
text_file.close()

print("Success!\nBach message created.")

#For debugin
# plt.imshow(img_bin, cmap="gray")
# plt.show()