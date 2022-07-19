import tkinter
import os
import subprocess
import time
import sys
import datetime
import colorama
from shutil import copyfile
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox as messagebox
import threading


#Initialize Vars. Do not modify unless you are using a custom FFMPEG or xCON build
current = 0
count = 0
start = 0
end = 0
pause = False
sampleMode = 'swr'

#Set this to the folder containing a folder that contains your samples. No ncw should be directly in this dir, only a folder containing them.
#Designed this way to easily accomodate direct ncx unpacking into this dir. 
rootdir = os.path.dirname(os.path.realpath(__file__)) + "/Resources/Default"
micTarget = ["!"]
#micTarget = ["ab,","close1","close2","close","surround","AB","CLOSE1","CLOSE2","CLOSE","SRND","SUR","SURROUND"]   #Mic positions you want to delete. Case sensitive, type exactly as is in the filename.
whitelist = ["!null"]  #Samples containing these words are ignored and not processed.
doShrink = False
print("Starting application...")
print("For some reason the program runs slower if I don't keep the cmd line open. Not sure why, don't care enough to fix it")
print("So for now this window will remain open. You can ignore it entirely, unless something breaks in which case")
print("an error message might pop up here which you should look at and contact me about.")
colorama.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

xCon = resource_path("conNCW06.exe")
ffmpeg = resource_path("ffmpegReduced.exe")
micReplace = resource_path("micReplace.ncw")
#xCon = os.path.dirname(os.path.realpath(__file__)) + "/Resources/conNCW06.exe"
#ffmpeg = os.path.dirname(os.path.realpath(__file__)) + "/Resources/ffmpegReduced.exe"
#micReplace = os.path.dirname(os.path.realpath(__file__)) + "/Resources/micReplace.ncw"
print("Checking dependencies...")
print(xCon)
print(ffmpeg)
print(micReplace)

def getRootDir():
    global rootdir
    target = askdirectory(title='Select Samples Folder') # shows dialog box and return the path
    rootdir = (str(target))
    displayRootDir.set("Current Dir: " + str(target))
    dirLabel.config(bg="green")
    dirLabel.config(font="none 12")

def submitMicTarget():
    global micTarget
    entered_text=micTargetEntry.get()
    micTargets.set("Mic targets: " + str(entered_text))
    micLabel.config(bg="green")
    micLabel.config(font="none 12")
    micTarget = entered_text.split(",")

def submitMicWhitelist():
    global whitelist
    entered_text=micWhitelistEntry.get()
    micWhitelist.set("Mic Whitelist: " + str(entered_text))
    whitelistLabel.config(bg="green")
    whitelistLabel.config(font="none 12")
    whitelist = entered_text.split(",")

def changedoShrink():
    global doShrink
    if doShrink is False:
        doShrink = True
        do16Bit.set("True")
        shrinkLabel.config(bg="green")
    elif doShrink is True:
        doShrink = False
        do16Bit.set("False")
        shrinkLabel.config(bg="red")

def changeMode():
    global sampleMode
    if (sampleMode is 'swr'):
        sampleMode = 'soxr'
        modeLabel.config(bg='magenta')
        modeVar.set("Mode: soxr - Way Slower, slightly higher quality")
    elif (sampleMode is 'soxr'):
        sampleMode = 'swr'
        modeLabel.config(bg='blue')
        modeVar.set("Mode: swr - Way Faster, slightly lower quality")
def onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


def scan():
    global count
    count = 0
    print("Beginning Stage A: Pre-Startup")
    print("Scanning For samples...")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("ncw"):
                count += 1
            else:
                print("NON ncw file: " + os.path.join(subdir,file) + " found")
                #os.remove(os.path.join(subdir,file))
    print(str(count) + " Samples found.")


def osWalk():
    global count
    global current
    current =0
    print("Beginning Stage B: Mic Deletion and File Shrinking")
    print("Targeting Samples...")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if (pause != True):
                if file.endswith("ncw"):
                    current += 1
                    runOutput.set("Processing file: " + str(current) + " of " + str(count))
                    runOutputFile.set("File: " + file)
                    if micDelete(subdir, file) is False:
                        #print('(' + str(current) + ' / ' + str(count) + ') ', end='')
                        if doShrink is True:
                            print('(' + str(current) + ' / ' + str(count) + ')',end='')
                            shrink(subdir,file)
            else:
                print("Paused")
                time.sleep(1)
                
def shrink(subdir,file):
        subprocess.call([xCon,os.path.join(subdir,file)],shell=False)
        print("\033[A\033[A")
        if (sampleMode is 'soxr'):
            subprocess.call([ffmpeg, '-hide_banner', '-loglevel', 'error','-y','-i', os.path.join(subdir, file.replace('ncw','wav',1)),'-acodec', 'pcm_s16le', '-af', 'aresample=resampler=soxr:osf=s16:dither_method=triangular', '-nostdin',os.path.join(subdir, "C" + file.replace('ncw','wav',1))],shell=False)
        elif (sampleMode is 'swr'):
            subprocess.call([ffmpeg, '-hide_banner', '-loglevel', 'error','-y','-i', os.path.join(subdir, file.replace('ncw','wav',1)),'-acodec', 'pcm_s16le', '-af', 'aresample=osf=s16:dither_method=triangular', '-nostdin',os.path.join(subdir, "C" + file.replace('ncw','wav',1))],shell=False)

        os.remove(os.path.join(subdir,file.replace('ncw','wav',1)))
        os.remove(os.path.join(subdir,file))
        os.rename(os.path.join(subdir, "C" + file.replace('ncw','wav',1)),os.path.join(subdir, file.replace('ncw','wav',1)))
        subprocess.call([xCon,os.path.join(subdir,file.replace('ncw','wav',1))],shell=False)
        print("\033[A\033[A")
        os.remove(os.path.join(subdir,file.replace('ncw','wav',1)))
def micDelete(subdir, file):
    if not any(ignore in file for ignore in whitelist) and any(mic in file for mic in micTarget):
        copyfile(micReplace, os.path.join(subdir,file))
        print("Removing file: " + os.path.join(subdir,file))
        print("\033[A")
        return True
    else:
        return False

def pack(subdir, file):
    subprocess.call([xCon,os.path.join(subdir,file)],shell=False)

def close():
    window.destroy()

def pauseScript():
    global pause
    if pause is False:
        pause = True
        pauseButton.config(text="Resume Script")
        pauseButton.config(bg="green")
    elif pause is True:
        pause = False
        pauseButton.config(text="Pause")
        pauseButton.config(bg="red")

def destroyLabels():
    global current
    global count
    global start
    global end
    l1.destroy()
    l2.destroy()
    l3.destroy()
    l4.destroy()
    l5.destroy()
    l6.destroy()
    l7.destroy()
    l8.destroy()
    l9.destroy()
    l10.destroy()
    l11.destroy()
    l12.destroy()
    l13.destroy()
    l14.destroy()
    button.destroy()
    dirLabel.destroy()
    micLabel.destroy()
    micTargetEntry.destroy()
    whitelistLabel.destroy()
    micWhitelistEntry.destroy()
    shrinkLabel.destroy()
    modeLabel.destroy()
    dirnew = tkinter.Label(window,textvariable= displayRootDir,bg="green",fg="white",font="none 12 bold")
    dirnew.grid(row=0,column=0,sticky=W)
    lnew = Label(window,text="Running script!",bg="black",fg="white",font="none 12 bold")
    lnew.grid(row=1,column=0,columnspan=2)
    runlog = tkinter.Label(window,textvariable= runOutput,bg="green",fg="white",font="none 12 bold")
    runlog.grid(row=2,column=0,sticky=W)
    runlog2 = tkinter.Label(window,textvariable= runOutputFile,bg="black",fg="white",font="none 12 bold")
    runlog2.grid(row=3,column=0,sticky=W)
    run()
    pauseButton.grid(row=4,column=0,sticky=W)
    closeButton = Button(window,text="Close Program",command=close,bg="red",fg="white",font="none 12 bold")
    closeButton.grid(row=5,column=0,sticky=W)

    startl = tkinter.Label(window,textvariable= str(start),bg="green",fg="white",font="none 12 bold")
    startl.grid(row=6,column=0,sticky=W)    
    endl = tkinter.Label(window,textvariable= end,bg="green",fg="white",font="none 12 bold")
    endl.grid(row=7,column=0,sticky=W)    


def run():
    t = threading.Thread(target=runSub)
    t.setDaemon(True)
    t.start()

def runSub():
    global start
    global end
    begin = time.time()
    print(str(begin))
    start.set("Script start at: " + datetime.datetime.now().strftime("%X"))
    print(start)
    scan()
    osWalk()
    stop = time.time()
    end.set("Shrink finished in: " + str(datetime.timedelta(seconds=int(stop - begin))))
    print("Shrink finished in: " + str(datetime.timedelta(seconds=int(stop - begin))))

window = tkinter.Tk()
displayRootDir = StringVar()
micTargets = StringVar()
do16Bit = StringVar()
micWhitelist = StringVar()
runOutput = StringVar()
runOutputFile = StringVar()
start = StringVar()
end = StringVar()
modeVar = StringVar()
pauseButton = Button(window,text="Pause Program (Buggy!)",command=pauseScript,bg="red",fg="white",font="none 12 bold")

micTargets.set("No Current Mic Targets. This is ok if you do not want to delete any mics.")
micWhitelist.set("No Current Whitelist. This is ok if you do not want to whitelist anything")
displayRootDir.set("WARNING! Current Dir: No Selected Directory. Select one with the button!")
do16Bit.set("False")
runOutput.set("0/0")
runOutputFile.set("No Output File Selected")
end.set("Script in progress....")
modeVar.set("Mode: swr - Way Faster, slightly lower quality")
window.title("KonTinkerer v.0.2")
window.configure(background='black')
window.geometry('600x600')
window.resizable(width=False, height=False)
#bgPhoto = PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "\Resources\\icon.png")
#Label(window, image=bgPhoto,bg ="black").grid(row=0,column=0,sticky=W)
l1 = Label(window,text="Please select your Sample Library Directory",bg="black",fg="white",font="none 12 bold")
l1.grid(row=1,column=0,sticky=W)
button = Button(window, text="Select (Click me)", command=getRootDir,bg="green",fg="white",font="none 12 bold")
button.grid(row=3,column=0,sticky=W)
dirLabel = tkinter.Label(window,textvariable= displayRootDir,bg="red",fg="white",font="none 12 bold")
dirLabel.grid(row=2,column=0,sticky=W)
l2 = Label(window,text="",bg="black",fg="black")
l2.grid(row=4,column=0,sticky=W)

l3 = Label(window,text="Input the mic positions / articulations you want to delete as shown below:",bg="black",fg="white",font="none 12 bold")
l3.grid(row=5,column=0,sticky=W)
micLabel = tkinter.Label(window,textvariable = micTargets,bg="red",fg="white",font="none 12 bold")
micLabel.grid(row=6,column=0,sticky=W)
l4 = Label(window,text="Example: surround,sur,AB,close1,spot",bg="black",fg="white",font="none 12")
l4.grid(row=7,column=0,sticky=W)
micTargetEntry = Entry(window, width=20, bg="white", font="none 12 bold")
micTargetEntry.grid(row=8,column=0,sticky=W)
l5 = Button(window,text="SUBMIT",width=6,command=submitMicTarget)
l5.grid(row=9,column=0,sticky=W)
l6 = Label(window,text="",bg="black",fg="black")
l6.grid(row=10,column=0,sticky=W)


l7 = Label(window,text="Input the mic positions / articulations you want to whitelist as shown below:",bg="black",fg="white",font="none 12 bold")
l7.grid(row=11,column=0,sticky=W)
whitelistLabel = tkinter.Label(window,textvariable = micWhitelist,bg="red",fg="white",font="none 12 bold")
whitelistLabel.grid(row=12,column=0,sticky=W)
l8 = Label(window,text="Example: CLOSE2",bg="black",fg="white",font="none 12")
l8.grid(row=13,column=0,sticky=W)
micWhitelistEntry = Entry(window, width=20, bg="white", font="none 12 bold")
micWhitelistEntry.grid(row=14,column=0,sticky=W)
l9 = Button(window,text="SUBMIT",width=6,command=submitMicWhitelist)
l9.grid(row=15,column=0,sticky=W)
l10 = Label(window,text="",bg="black",fg="black")
l10.grid(row=16,column=0,sticky=W)


l11 = Label(window,text="Convert files to 16bit? (Click below to toggle)",bg="black",fg="white",font="none 12 bold")
l11.grid(row=17,column=0,sticky=W)
shrinkLabel = Button(window,textvariable= do16Bit,bg="red",fg="white",font="none 12 bold",command=changedoShrink)
shrinkLabel.grid(row=18,column=0,sticky=W)
l12 = Label(window,text="",bg="black",fg="black")
l12.grid(row=19,column=0,sticky=W)
l13 = Label(window,text="",bg="black",fg="black")
l13.grid(row=20,column=0,sticky=W)

modeLabel = Button(window,textvariable= modeVar,bg="blue",fg="white",font="none 12 bold",command=changeMode)
modeLabel.grid(row=21,column=0,sticky=W)
l14 = Button(window,text="RUN SCRIPT (ONLY RUN IF YOU HAVE CHOSEN ALL OPTIONS ABOVE",command=destroyLabels,bg="red",fg="white",font="none 12 bold")
l14.grid(row=22,column=0,sticky=W)



window.protocol("WM_DELETE_WINDOW", onClosing)
window.mainloop()





