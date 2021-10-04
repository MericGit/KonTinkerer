import ffmpeg
import os
rootdir = "C:\\Users\\dongd\\Downloads\\testffmpeg\\input\\"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith("wav"):
            print(os.path.join(subdir, file))
            print('ran')
            os.system("C:\\ffmpeg\\bin\\ffmpeg.exe -hide_banner -loglevel error -i " + os.path.join(subdir, file) + " -acodec pcm_s16le -af aresample=osf=s16:dither_method=rectangular -nostdin " + "C:\\Users\\dongd\\Downloads\\testffmpeg\\test2\\" + file )
