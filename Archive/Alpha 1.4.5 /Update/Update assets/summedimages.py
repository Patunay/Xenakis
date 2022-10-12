import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageGrab

# Summ of layers


# Initialize 2 arrays with same size

# invert 1 and 0s
#   - Now 1 represets event and 0 represent nothing 

# add them, check result:
#   - 0s should be white space
#   -1s should be event
# If all ok:
#   - Invert 1s and 0s again
####################################
# # Initialize canvas = all 0s
# canvas = np.array([[0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0]])



# Arrays to be combined:
a = np.array([[1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1],
              [1,0,0,1,1,0,0,1],
              [1,0,0,1,1,0,0,1]])

b = np.array([[1,1,1,0,0,1,1,1],
              [1,1,1,0,0,1,1,1],
              [1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1]])


print(a,"\n")
print(b,"\n")

a = a^1     # Invert values
b = b^1

c = a + b   # Add arrays
print(c,"\n")

c = c^1 #   Convert result
print(c,"\n")


plt.imsave('/Users/cmauro/Documents/Programs/Xenakis/Update/temp_file/temp_preview.png',c,cmap="gray")   # save the array to .png 


# Calculate appropiate clef for given input