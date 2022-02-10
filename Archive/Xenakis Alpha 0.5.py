from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import itertools

voices = input("Enter number of voices ")
voices = int(voices)         #number of 3rd dimensions
voiceloop = np.arange(voices-1)

counter = 1
print()
print ("Enter filepath of voice", counter)
filepath = input()
counter = counter + 1

seed = np.array(Image.open(filepath))      #opening voice 1 (seed)
blue = seed[:,:,2]                         #obtaining Blue values
threshold = 195
binarized = 1.0 * (blue > threshold) # make all pixels 1 < threshold black



plt.imshow(binarized, cmap="gray")
plt.show()


out = binarized.copy()

res = []
for rowIdx, row in enumerate(out):
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
##############################################BIEN


msr =  result.shape
msr = np.array(msr)

i = msr[0] /2
final = np.split(result, i)


end_array = np.arange(i) #gets number of iterations necessary for for loop

x = 0     #sub array number   Counter goes up every iteration until i ("end")

comp = []  #storage of durations

for p in end_array:
    comp.append((final[x][1,1])-(final[x][0,1])+1)     #get duration    (refers to specific objects in sub arrays)
    x = x + 1                                          #counter of sub array
x = 0                                                  #Resets counter to 0
comp_array = np.array(comp)
comp_array = comp_array[:,np.newaxis]



ot = result[::2]   #Gets starting onset and pitch
ot[:,[1,0]] = ot[:,[0,1]]  #Swaps places of colums 


# SUM EVERYTHING
OUTPUT = np.concatenate((ot,comp_array), axis=1)

OUTPUT = OUTPUT[np.lexsort(np.fliplr(OUTPUT).T)]   #Ascending order///In Chronological Order

#############################################
# Escaling

pitches1 = OUTPUT[:,1]  #gets 2nd column

mod = 176                 #88x2 (piano notes+ quartertones) 
min = np.amin(pitches1)     #Get min1
max = np.amax(pitches1)      #Get Max

index = min + max             #Get inversion index

OUTPUT[:,1] = (((index - OUTPUT[:,1]) % mod)/2)*100

#Handle Onsets and Durations
OUTPUT[:,0] = OUTPUT[:,0]*250
OUTPUT[:,2] = OUTPUT[:,2]*250
OUTPUT = OUTPUT.astype("int64")

#####
# Deletion of first 2 items   DEPENDS ON # OF GUIDES!!!!!!


OUTPUT = np.delete(OUTPUT,[0,1], axis=0)
end_array = np.delete(end_array,[0,1], axis=0)




i = i - 2
sintax = np.split(OUTPUT, i)



#########################
counter2 = 1
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

counter2 = str(counter2)
pred = "addchords[" + counter2
counter2 = int(counter2)

bachroll1 = pred + string

###############################


#####################
product = OUTPUT
 


#####################################################################
#####################################################################
#####################################################################
#####################################################################
#####################################################################
bachvoices = []
raw = []   #Initialize empty list where all voices will be stored

for total in voiceloop:         #Start of Macro-Loop

    print ("Enter filepath of voice", counter)
    filepath = input()
    counter = counter + 1

    tree = np.array(Image.open(filepath))   #Tree var will store arrays and will be aupdated for every loop
    blue = tree[:,:,2]                      #obtaining Blue values
    temp_array = 1.0 * (blue > threshold)   # make all pixels 1 < threshold black  

########################

    out = temp_array.copy()

    res2 = []
    for rowIdx, row in enumerate(out):
        colIdx = 0                       #start column index
        for k, grp in itertools.groupby(row):
            vals = list(grp)                   #Values in the group
            lgth2 = len(vals)                  #Lenght of the group
            colIdx2 = colIdx + lgth2 - 1       #end of column index

            if k == 0 and lgth2 >= 2:           #Record this group if under threshhold
                res2.append([rowIdx,colIdx])
                res2.append([rowIdx, colIdx2])
            colIdx = colIdx2 + 1              #Advance column index
    result2 = np.array(res2)

    msr2 =  result2.shape
    msr2 = np.array(msr2)

    i2 = msr2[0] /2
    final2 = np.split(result2, i2)


    end_array2 = np.arange(i2) #gets number of iterations necessary for for loop

    comp2 = []  #storage of durations

    for p in end_array2:
        comp2.append((final2[x][1,1])-(final2[x][0,1])+1)     #get duration    (refers to specific objects in sub arrays)
        x = x + 1                                         #counter of sub array
    x = 0                                                 #Resets counter to 0
    comp_array2 = np.array(comp2)
    comp_array2 = comp_array2[:,np.newaxis]

    ot2 = result2[::2]   #Gets starting onset and pitch
    ot2[:,[1,0]] = ot2[:,[0,1]]  #Swaps places of colums 

    # print(ot.shape)
    # print(comp_array.shape)

    # print(ot2.shape)
    # print(comp_array2.shape)

    OUTPUT2 = np.concatenate((ot2,comp_array2), axis=1)
    #Ascending order///In Chronological Order
    OUTPUT2 = OUTPUT2[np.lexsort(np.fliplr(OUTPUT2).T)]


    # Escaling

    OUTPUT2[:,1] = (((index - OUTPUT2[:,1]) % mod)/2)*100

    #Handle Onsets and Durations
    OUTPUT2[:,0] = OUTPUT2[:,0]*250
    OUTPUT2[:,2] = OUTPUT2[:,2]*250
    OUTPUT2 = OUTPUT2.astype("int64")

    #####
    # Deletion of first 2 items

    
    OUTPUT2 = np.delete(OUTPUT2,[0,1], axis=0)
    end_array2 = np.delete(end_array2,[0,1], axis=0)
    i2 = i2 - 2
    


    raw.append(OUTPUT2)


    tempfix = OUTPUT2.shape
    # print(tempfix)
    tempfix = np.array(tempfix)
    i2 = tempfix[0]
    # print(i2)


    sintax2 = np.split(OUTPUT2, i2)

    # print(sintax2)
    counter2 = str(counter2)

    bachvoices.append("addchords[")
    bachvoices.append(counter2)
    counter2 = int(counter2)

    counter2 = counter2 + 1

    s2 = []
    for q2 in end_array2:
        s2.append("[")                                 #[
        s2.append(sintax2[x][0,0])                     #[ onset
        s2.append("[")                                #[ onset [
        s2.append(sintax2[x][0,1])                     #[ onset [ pitch
        s2.append(" ")                                # space
        s2.append(sintax2[x][0,2])                     #[ onset [ pitch duration
        s2.append(" ")                                # space
        s2.append("100]]")                            #[ onset [ pitch duration 100]
        x = x + 1                #go to next sub-array
    s2.append("]")                #final "]"
    x = 0                        #Resets counter to 0
    string2 = "".join(map(str, s2)) #Join Everything
    bachvoices.append(string2)
    counter = int(counter)

bachvoicesprocessed = "".join(map(str, bachvoices)) #Join Everything

bach_output =  bachroll1 + bachvoicesprocessed 


text_file = open("BachrollInput.txt", "w")
text_file.write(bach_output)
text_file.close()

print("Succes!!!!!!")