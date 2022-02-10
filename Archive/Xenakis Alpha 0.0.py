from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import itertools

np.set_printoptions(suppress=True)   #Arrays avoid scientific notations

#####IT WORKS!!!!!!!!
########Manipulate threshold as needed, accept only png!, png as little as possible...

#Load Image as array

image = np.array(Image.open('/Users/cmauro/Documents/Programs/Scannerv2/Assets/layer2.png'))
########################################RGB VALUES

red = image[:,:,0]    #obtaining Red values
green = image[:,:,1]  #obtaining Green values
blue = image[:,:,2]   #obtaining Blue values

##########################################Convert to Greyscale

threshold = 195
binarized = 1.0 * (green > threshold) ## make all pixels 1 < threshold black
plt.imshow(binarized, cmap="gray")   #DISPLAY GREYSCALE
#SAVE AS FORMAT: [Tittle of text file, array to be saved, delimiter character]
#np.savetxt("ChartBin.txt", binarized, fmt="%0.10g", delimiter=",")######keep for future reference
plt.show()

#########################################Convert to Binary

out = binarized.copy()

res = []
for rowIdx, row in enumerate(out):
    colIdx = 0 #start column index
    for k, grp in itertools.groupby(row):
        vals = list(grp)                   #Values in the group
        lgth = len(vals)                  #Lenght of the group
        colIdx2 = colIdx + lgth - 1       #end of column index

        if k == 0 and lgth >= 2:           #Record this group if under threshhold
            res.append([rowIdx,colIdx])
            res.append([rowIdx, colIdx2])
        colIdx = colIdx2 + 1              #Advance column index
result = np.array(res)

###################Get i

msr =  result.shape
msr = np.array(msr)

i = msr[0] /2
final = np.split(result, i)

###################

end_array = np.arange(i) #gets number of iterations necessary for for loop

x = 0     #sub array number   Counter goes up every iteration until i ("end")

comp = []  #storage of durations

for p in end_array:
    comp.append((final[x][1,1])-(final[x][0,1])+1)     #get duration    (refers to specific objects in sub arrays)
    x = x + 1                                          #counter of sub array
x = 0                                                  #Resets counter to 0
comp_array = np.array(comp)
comp_array = comp_array[:,np.newaxis]

#####################
#Get Output
#####################

ot = result[::2]   #Gets starting onset and pitch
ot[:,[1,0]] = ot[:,[0,1]]  #Swaps places of colums 


# SUM EVERYTHING
OUTPUT = np.concatenate((ot,comp_array), axis=1)
print(OUTPUT)
#Ascending order///In Chronological Order
OUTPUT = OUTPUT[np.lexsort(np.fliplr(OUTPUT).T)]
# np.savetxt("OUTPUT.csv", OUTPUT, fmt="%0.10g", delimiter=" ")

#############################################

# Exponential scaling   

#Handle Pitches
pitches = OUTPUT[:,1]  #gets 2nd column

mod = 176                 #88x2 (piano notes+ quartertones) 
min = np.amin(pitches)     #Get min
max = np.amax(pitches)      #Get Max
index = min + max             #Get inversion index

OUTPUT[:,1] = (((index - OUTPUT[:,1]) % mod)/2)*100

#Handle Onsets and Durations
OUTPUT[:,0] = OUTPUT[:,0]*250
OUTPUT[:,2] = OUTPUT[:,2]*250
OUTPUT = OUTPUT.astype("int64")

print(OUTPUT)
#################################################
###Create TXT file
# np.savetxt("DATA.txt", OUTPUT, fmt="%0.10g", delimiter=" ")

print(np.shape(OUTPUT))

####################################Creation bach.roll string

print(np.size(end_array))
sintax = np.split(OUTPUT, i)

#########################
s = []
for q in end_array:
    s.append("[")                                #[
    s.append(sintax[x][0,0])                     #[ onset
    s.append("[")                                #[ onset [
    s.append(sintax[x][0,1])                     #[ onset [ pitch
    s.append(" ")                                # space
    s.append(sintax[x][0,2])                     #[ onset [ pitch duration
    s.append(" ")                                # space
    s.append("100]]")                            #[ onset [ pitch duration 100]
    x = x + 1                #go to next sub-array
s.append("]")                #final "]"
x = 0                        #Resets counter to 0
string = "".join(map(str, s)) #Join Everything

pred = "addchords[1"

Bachroll = pred + string
# print(Bachroll)


text_file = open("BachrollInput.txt", "w")
text_file.write(Bachroll)
text_file.close()

print("Succes!!!!!!")

##########
##########
##########
###END####
##########
##########

"""
Next steps:

Multiple instruments!  (up to 10 voices? maybe infinate?)
Layers!!!:
1) Boundary layer [FIXED] Create Template with additional indications
2) 1st Voice     #All voices color black!!
3) 2nd Voice
:
:   n number of voices
:
[4) Velocity assignemnts?????] hypotetical for now


--------------
Request number of voices

create 3d array where 3rd dimension is voice assignment

iterate the process as many times as needed (lenght of 3rd dimension)


Keep polishing the multiplicators for all parameters
"""