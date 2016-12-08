from classify_data import convert
from music21 import *
import sys

# check for passed in arguments at the commandline
if len(sys.argv) != 2:
    exit('Usage: python script_name filename.jpg')

# obtain our notes list from the convert function
notes_list = convert()

# initialize a music21 stream
stream1 = stream.Stream()

# iterate through the notes and convert them into music21 format
for n in notes_list:
    new_note = note.Note(str(n[1]))
    new_note.duration = duration.Duration(float(n[0]))
    stream1.append(new_note)

# create an output file name based on the input file name
# this takes in the passed commandline argument, splits it at the decimal, and
# adds '.xml' to what was to the left of the decimal
savename = sys.argv[1].split('.')[0] + '.xml'

# save the stream to hard disk for reading by music software
stream1.write('musicxml', savename)
    
