import ffmpeg
import os
import subprocess
import time
import colorama
import datetime
from shutil import copyfile

#Initialize Vars. Do not modify unless you are using a custom FFMPEG or xCON build
colorama.init()
startTime = datetime.datetime.now()
current = 0
count = 0
xCon = os.path.dirname(os.path.realpath(__file__)) + "\Resources\conNCW04.exe"
ffmpeg = os.path.dirname(os.path.realpath(__file__)) + "\Resources\\ffmpegReduced.exe"

#Set this to the folder containing a folder that contains your samples. No ncw should be directly in this dir, only a folder containing them.
#Designed this way to easily accomodate direct ncx unpacking into this dir.
rootdir = "C:\\Users\\dongd\\Downloads\\JB\\Samples"
print("Script start: " + str(startTime))
micDelete = ["Close","Room"]


def scan():
    global count
    count = 0
    print("Beginning Stage A: Pre-startup")
    print("Scanning for samples...")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("ncw"):
                count+=1
            else:
                print("NON ncw file: " + os.path.join(subdir,file) + " found")
                #os.remove(os.path.join(subdir,file))
    print(str(count) + " Samples found.")



def shrink():
    global count
    global current
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("ncw"):
                current += 1
                print('(' + str(current) + ' / ' + str(count) + ') ', end='')
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


def test():    #In the future I will have the directory run through call a smaller method that shrinks individual files. This way I can have it 
               #All run through some main method loop which can let users pause the script at any time.
    while True:
        try:
            time.sleep(1)  # do something here
            print('.'),

        except KeyboardInterrupt:
            print('\nPausing...  (Hit ENTER to continue, type quit to exit.)')
            try:
                response = input()
                if response == 'quit':
                    break
                print ('Resuming...')
            except KeyboardInterrupt:
                print ('Resuming...')
                continue


start = time.time()
scan()
shrink()
end = time.time()
print("Shrink finished in: " + str(datetime.timedelta(seconds=int(end - start))))
