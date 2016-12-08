import numpy as np
import cv2
import sys
from findAndShow import find_show
import os
from shutil import rmtree
from config import templates

# check for passed in arguments at the commandline
if len(sys.argv) != 2:
    exit('Usage: python script_name filename.jpg')

# set the names of each image: one to analyze, two templates
image = sys.argv[1]
tem_name = templates[0]
template2 = templates[1]

# load the image
# the second argument is a color coding
# 1 is color, 0 is grayscale, -1 is unchanged
img_rgb = cv2.imread(image)

# check if the image was readable
if img_rgb is None:
    exit('The image to analyze was not readable')
print('Loaded image to analyze')

# convert to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# load the note template to look for
t = cv2.imread(tem_name, 0)

# check if the template for the notes was unreadable
if t is None:
    exit('The note template was unreadable')
print('Loaded note template')

# load the clef template to look for 
t2 = cv2.imread(template2, 0)

# check if the template for the clefs was unreadable
if t2 is None:
    exit('The clef template was unreadable')
print('Loaded clef template')

# check for the clefs in the image and store their (y) locations
print('Searching for clefs')
clef_list = find_show(t2, img_gray, img_rgb)

# keep our user updated
print "Located clefs, searching for notes"

# check for the tmp directory, in case it already exists, and get rid of it if it does
if os.path.isdir('./app/tmp'):
    rmtree('./app/tmp')

# create a temporary directory to hold all of the data to be classified
os.makedirs('./app/tmp/data')

# check the image for the notes so as to see where the lines are in the document
find_show(t, img_gray, img_rgb, clef=clef_list)
print('Notes found, highlighted on results.jpg')
