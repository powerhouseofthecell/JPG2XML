#!/bin/bash

# this finds the notes and stores them a temporary directory
python ./app/im_analyze.py $1

# this then takes those located notes and classifies them, before converting and writing
# to an xml file
python3 ./app/makemusic.py $1

# and this cleans up afterwards
python3 ./app/cleanup.py