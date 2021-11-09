import ffmpeg
import os
import subprocess
import time
rootdir = "C:\\Users\\dongd\\Downloads\\Temp\\Samples\\Collected-Samples\\Samples"
workingdir = "C:\\Users\\dongd\\Downloads\\Temp\\CSamples"

wavtoncw = True



count = 0
current = 0
print("Stage 0: Pre-startup")
time.sleep(2)
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith("wav"):
            count+=1
print(str(count) + " Samples found. \nBeginning Stage 1: Wav 24bit --> Wav 16bit")
time.sleep(2)

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith("wav"):
            current+=1
            print('Working... (' + str(current) + " / " + str(count) + ")")
            subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i',os.path.join(subdir, file), '-acodec', 'pcm_s16le', '-af', 'aresample=osf=s16:dither_method=rectangular', '-nostdin', os.path.join(workingdir,file)    ])

print("Stage 1: Wav 24bit --> Wav 16bit Completed")
print("Remember! Old directory and files are kept as a backup. Please delete after program completes")
print("Beginning Stage 2: Wav16bit --> ncw")
time.sleep(3)
if wavtoncw is True:
    current = 0
    subprocess.call(['conNCW04.exe', '-w2n',workingdir])
    print("Stage 2: Wav16bit --> ncw completed")
    print("Beginning Stage 3: Wav16bit deletion")
    time.sleep(2)
    for subdir, dirs, files in os.walk(workingdir):
        for file in files:
            if file.endswith("wav"):
                current+=1
                print('Working... (' + str(current) + " / " + str(count) + ")")
                os.remove(os.path.join(subdir, file))


    print("Stage 3 Wav16bit deletion completed!")
print("Shrinking has finished. Original samples are kept intact, remember to delete")