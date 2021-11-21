import ffmpeg
import os
import subprocess
import time
import shutil
import sys


rootdir = "C:\\Users\\dongd\\Downloads\\JB\\Samples"
workingdir = "C:\\Users\\dongd\\Downloads\\JB\\Samples2"
rootlast = rootdir.rsplit('\\',1)[-1]
workinglast = workingdir.rsplit('\\',1)[-1]


current = 0
count = 0
xCon = os.path.dirname(os.path.realpath(__file__)) + "\Resources\conNCW04.exe"
ffmpeg = os.path.dirname(os.path.realpath(__file__)) + "\Resources\\ffmpegFull.exe"
print(xCon)


def scan():
    global count
    count = 0
    print("\nBeginning Stage A: Pre-startup")
    print("Scanning for samples...")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("ncw"):
                count+=1
            else:
                print("NON ncw file: " + os.path.join(subdir,file) + " removed")
                os.remove(os.path.join(subdir,file))
    print(str(count) + " Samples found.")
    #self.update()

def ncwtowav():
    print("Beginning Stage B. Batch Compress ncw to wav")
    print("This will take a while....")
    for root, dirs, files in os.walk(rootdir):
        for d in dirs:
            path = os.path.join(rootdir,os.path.relpath(os.path.join(root, d), rootdir))
            print("TARGET: " + path)
            subprocess.call([xCon, '-n2w',path,path.replace(rootlast,workinglast,1)])


    print("\nBatch collecting finished. Deleting all old NCW files...")
    shutil.rmtree(rootdir)
    os.rename(workingdir,rootdir)

def shrink():
    global count
    current = 0
    print("Beginning Stage C: Wav 24bit --> Wav 16bit")
    def ignore_files(dir, files):
        return [f for f in files if os.path.isfile(os.path.join(dir, f))]

    shutil.copytree(rootdir,
                    workingdir,
                    ignore=ignore_files)

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("wav"):
                current+=1
                print('Working... (' + str(current) + " / " + str(count) + ")", end = "\r")
                subprocess.call([ffmpeg, '-hide_banner', '-loglevel', 'error','-y','-i', os.path.join(subdir, file),'-acodec', 'pcm_s16le', '-af', 'aresample=osf=s16:dither_method=rectangular', '-nostdin',os.path.join(subdir, file).replace(rootlast,workinglast,1)])

    print("Stage C: Wav 24bit --> Wav 16bit Completed")
def wavtoncw():
    global count
    current = 0
    print("Beginning Stage D: Wav16bit --> ncw")
    for root, dirs, files in os.walk(workingdir):
        for d in dirs:
            path = os.path.join(workingdir,os.path.relpath(os.path.join(root, d), workingdir))
            subprocess.call([xCon, '-w2n',path])
    print("Stage D: Wav16bit --> ncw completed")
    print("Beginning Stage E: Wav16bit deletion")
    time.sleep(2)
    for subdir, dirs, files in os.walk(workingdir):
        for file in files:
            if file.endswith("wav"):
                current+=1
                print('Working... (' + str(current) + " / " + str(count) + ")", end = "\r")
                os.remove(os.path.join(subdir, file))
    shutil.rmtree(rootdir)
    os.rename(workingdir,rootdir)



    print("Stage E Wav16bit deletion completed!")
    print("Shrinking has finished")

scan()
ncwtowav()
shrink()
wavtoncw()