# Starting Point module
from tkinter import *

import config

prg_name= config.prg_name
pgr_ver=config.pgr_ver

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
        config.algorithm_window_status = 1
        print("algorithm show status is ",config.algorithm_window_status)
        pass 

    #Go to Graph program
    def start_graph(self):
        config.graph_window_status = 1
        pass 

# stuff to run always here such as class/def
def main():
    welcome_window()
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   print("Standalone Launch")
    # stuff only to run when not called via 'import' here
   root = Tk()
   welcome_window(root,prg_name +" "+ pgr_ver,pgr_ver)
   main()


