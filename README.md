# ShrinkRay
Easily shrink the disk space that a Kontakt library takes!


This script batch converts ncw files from a directory down from 24bit to 16bit. Kontakt lib developers most commonly use 24bit samples in their recordings, however these take up much more space than 16bit files, and work worse with ncw compression. By converting from 24bit to 16bit we we can almost always at least halve the disk space that a library takes up!

# WARNING:
The conversion process at the moment is not optimized. What this means is that you will require 3x the original library size during the conversion process. This can be problematic for large libraries, but you can totally just convert the library in parts if space is a problem. After the conversion process is finished the space taken will be halved so it becomes less of a problem as time goes on. The general process is this

Library Initial Size: 1x

Library Decompress to Wav Size + Initial Size: 3x

Delete Initial ncw samples: 2x

Shrink Wav24bit to 16bit: 3x

Delete Wav 24bit: 1x

Convert Wav16bit into NCW: 1.5x

Delete Wav16bit: 0.5x

As you can see this is done on a per-directory basis rather than a per file basis. If done on a per-file basis than you would not need any extra space to decompress and shrink files. That is a work in progress feature for the future. For now just shrink in parts. 



## Downsides:  

During this process a slight dither is added to preserve the quality of the audio file during the conversion, however do note that this will slightly raise the noise floor. For the vast majority of cases this will be imperceptible to every user, with it often only occuring at around -80db. 

Additionally, 16bit files produce a few more artifacts in Time Machine compared to 24bit, however this will only be noticeable in extreme cases when you really warp the sound.

### Steps: 

There are a few things you will need to do in advance for this script. If you have a Kontakt Player library that is encoded and has the samples in NKX format you will need to manually unpack the NKX containers into the ncw containers.

If your library does not have its samples stored in NKX containers, disregard steps 1-2.

1. To do so you should use this utility:
http://www.mediafire.com/file/p94ilctiajpdi9q/Total_Commander_9.5.1_and_inNKX_1.2.1.rar/file 

    This downloads TotalCommander (A sort of windows file explorer) + A plugin you can use in Total commander to unpack NKX.

    Install instructions are provided in the link.


2. A guide on how to use it is here:
https://youtu.be/Il8_Mx3-A-0?t=89

    Please note, this is not officially supported by Kontakt or devs, and it may go against the EULA. Use at your own risk! (It is doubtful though that Kontakt will care about this)

3. Next, open the shrinkStandalone.py file and edit the filepaths so that rootdir points towards the samples folder of the files you wish to convert. Workingdir can be set to whatever you want, so long as that folder does not already exist. I suggest just making it exist in the same root directory as wherever your samples folder you are targetting is stored.

4. Now run the python script and wait. The conversion process may take a while depending on the size of the library, and your computers specs. The script must run through thousands of audio files multiple times (NCW --> Wav24bit --> Wav16bit --> NCW), so it takes a while.

5. Enjoy your new shrunk library! You can use inNKX and Total Commander to repackage your new samples into NKX containers, or just leave it as be. Replace the original samples directory of the library with the new one that ShrinkRay made, and remember to batch re-save the library. (If you repacked into NKX this is a required step. Optional for NCW but highly recommended)


# Upcoming Features
I am working on developing a simple executbale using PyQt so you will not have to manually edit the file for the filepaths, or have to suffer from pasting the paths as command line arguments.

This is a WIP feature and may take a while as I learn how to use PyQt

Additionally others are working on ways to unpack NKX without inNKX and Total Commander. If they finish this I will incorporate it into this script so users can skip the manual steps related to NKX containers.



# Dependencies
- Python 3
- A few Python modules (requirements.txt provided). 

pip install -r /path/to/requirements.txt

- FFmpeg (Included in the download)
- conNCW04 (Included in the download)
