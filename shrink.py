import ffmpeg
import os
rootdir = 'C:\\Users\\dongd\\Downloads\\testffmpeg'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith("wav"):
            print(os.path.join(subdir, file))
            print('ran')
            os.system("ffmpeg -i" + file + "-acodec wav -af aresample=osf=s16:dither_method=rectangular" + "output.wav")
