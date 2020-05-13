# DSProject
Our DSL DSP Combined Term Project! 
by Akarsh Kumar, Sunny Kharel ...[insert ur name]

We are trying to seperate mixed audio signals into its component parts. 
The example we are dealing with is seperating an audio signal into one or more speech and noise signals.




Notes: 
common_audio.py is a file with common useful audio functions we all should have. Import into notebooks like this:
'from common_audio import *'

Most audio datasets are just a directory of directories of files (.wav/.flac/.mp3). 
audio_dataset.py is there to account for this cleanly in code.
'from audio_dataset import *'

It recursively finds all sound files and organizes them into a list of files. Whenever you want to load specific files (or the next batch of k files), simply call ds.load([1,2,100,399]), and it will return the loaded audio clips.
