import ffmpeg
import os
import subprocess
import time
import shutil
import sys
import colorama


rootdir = "C:\\Users\\dongd\\Downloads\\JB\\Samples"
workingdir = rootdir + "2"
rootlast = rootdir.rsplit('\\',1)[-1]
workinglast = workingdir.rsplit('\\',1)[-1]
colorama.init()


current = 0
count = 0
xCon = os.path.dirname(os.path.realpath(__file__)) + "\Resources\conNCW04.exe"
ffmpeg = os.path.dirname(os.path.realpath(__file__)) + "\Resources\\ffmpegReduced.exe"
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
                print(os.path.join(subdir,file), end = "\r")
            else:
                print("NON ncw file: " + os.path.join(subdir,file) + " removed")
                os.remove(os.path.join(subdir,file))
    print("\n" + str(count) + " Samples found.")

def shrink():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("ncw"):
                subprocess.call([xCon,os.path.join(subdir,file)])
                print("\033[A\033[A")

                subprocess.call([ffmpeg, '-hide_banner', '-loglevel', 'error','-y','-i', os.path.join(subdir, file.replace('ncw','wav',1)),'-acodec', 'pcm_s16le', '-af', 'aresample=osf=s16:dither_method=rectangular', '-nostdin',os.path.join(subdir, "C" + file.replace('ncw','wav',1))])
                os.remove(os.path.join(subdir,file.replace('ncw','wav',1)))
                os.remove(os.path.join(subdir,file))
                os.rename(os.path.join(subdir, "C" + file.replace('ncw','wav',1)),os.path.join(subdir, file.replace('ncw','wav',1)))
                subprocess.call([xCon,os.path.join(subdir,file.replace('ncw','wav',1))])
                print("\033[A\033[A")
                os.remove(os.path.join(subdir,file.replace('ncw','wav',1)))
            else:
                print("NON ncw file located in directory - Ignoring file: " + os.path.join(subdir,file))


shrink()