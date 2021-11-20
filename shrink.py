import ffmpeg
import os
import subprocess
import time
import shutil
rootdir = "C:\\Users\\dongd\\Downloads\\JB\\Samples"
workingdir = "C:\\Users\\dongd\\Downloads\\JB\\Samples2"
rootlast = rootdir.rsplit('\\',1)[-1]
workinglast = workingdir.rsplit('\\',1)[-1]

ncwtowav = True
shrink = True
wavtoncw = True
current = 0
count = 0




if ncwtowav is True:
    print("\nBeginning Stage A: Pre-startup")
    print("Scanning for samples...")
    time.sleep(2)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("ncw"):
                count+=1
    print(str(count) + " Samples found. \nBeginning Stage B. Batch Compress ncw to wav")
    print("This will take a while....")
    for root, dirs, files in os.walk(rootdir):
        for d in dirs:
            path = os.path.join(rootdir,os.path.relpath(os.path.join(root, d), rootdir))
            print("\n" + path)
            subprocess.call(['conNCW04.exe', '-n2w',path,path.replace(rootlast,workinglast,1)])
    print("\nBatch collecting finished. Deleting all old NCW files...")
    shutil.rmtree(rootdir)
    os.rename(workingdir,rootdir)

if shrink is True:
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
                subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'error','-y','-i', os.path.join(subdir, file),'-acodec', 'pcm_s16le', '-af', 'aresample=osf=s16:dither_method=rectangular', '-nostdin',os.path.join(subdir, file).replace(rootlast,workinglast,1)])

    print("Stage C: Wav 24bit --> Wav 16bit Completed")
    time.sleep(1)
if wavtoncw is True:
    
    print("Beginning Stage D: Wav16bit --> ncw")
    for root, dirs, files in os.walk(workingdir):
        for d in dirs:
            path = os.path.join(workingdir,os.path.relpath(os.path.join(root, d), workingdir))
            subprocess.call(['conNCW04.exe', '-w2n',path])
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