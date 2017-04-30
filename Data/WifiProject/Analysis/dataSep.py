from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)

with open(filename,"r") as f:
    for line in f:
        #print(line)
        #print(line.split(','))
        outf = open("day"+line.split(',')[1]+".csv",'a')
        outf.write(line)
        outf.close()
print("done")
