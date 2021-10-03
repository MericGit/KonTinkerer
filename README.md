# ShrinkRay
Easily shrink the disk space that a Kontakt library takes!


This script batch converts wav files from a directory down from 24bit to 16bit. Kontakt lib developers most commonly use 24bit samples in their recordings, however these take up much more space than 16bit files, and work worse with ncw compression. By converting from 24bit to 16bit we we can almost always at least halve the disk space that a library takes up!


### Downsides:  

During this process a slight dither is added to preserve the quality of the audio file during the conversion, however do note that this will slightly raise the noise floor. For the vast majority of cases this will be imperceptible to every user, however it will be most noticeable on "quiet" libraries. I.E. felt pianos, soft dynamic textural libs, etc. It should still almost be indistinguishable however.

Additionally, 16bit files produce a few more artifacts in Time Machine compared to 24bit, however this will only be noticeable in extreme cases when you really warp the sound.

#### Steps: 

There are a few things you will need to do in advance for this script. You'll need to perform a batch collect samples with Kontakt in order to convert the original ncw or nkx files into wav files. This can be done in Kontakt. 

![image](https://user-images.githubusercontent.com/41242144/135735789-94cdb0e9-8b11-484e-8973-184d3fdbf25e.png)

Select yes to the erase multi prompt (It will just clear the currently loaded instruments)
In the prompt, select your input directory as the library you want to convert, and select an output directory. I recommend a new dedicated empty folder for this. 


![image](https://user-images.githubusercontent.com/41242144/135735873-df605288-0f6b-4628-8ce4-8fa6527aadf4.png)

Choose Collect Samples, and uncompressed WAV / AIF

Click Convert

Wait for the batch collecting to finish, then navigate to the output directory you chose. Go to Collected Samples --> Samples. Run ShrinkRay on this folder.

Then run Batch Collect again and choose the directory that you ran shrinkray on as your input directory, and select a new output directory, but this time choose Lossless Compressed NCW for your Destination Sample Format. 

Now you have your newly converted, reduced size samples. Replace your original libraries samples with these, and delete the wav sampples created earlier. 
