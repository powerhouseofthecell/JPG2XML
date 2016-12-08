import numpy as np
from classify_note_pitch import classifyPitch
from classify_note_length import classifyLength, targetSize

def convert():
    # this converts the classified data from a numpy array to a python list
    pitches = classifyPitch().tolist()
    lengths = classifyLength().tolist()

    # this creates keys for the data, which is returned as numbers that correspond
    # to indices
    # additionally, note that the first character is the pitch
    # and the second is the octave
    pitch_key = ['a4', 'b4', 'c5', 'd4', 'd5', 'e4', 'e5', 'f4', 'f5', 'g4', 'g5']
    length_key = ['.5', '1.0']

    # this will convert the pitch list into a list of indices that can then be keyed
    pitch_indices = list()
    for row in pitches:
        # '1' demarcates the note value returned by the machine algorithm, so we
        # search for its index in each row
        try:
            pitch_indices.append(row.index(1))
        except:
            pitch_indices.append(0)
    # create a list that holds the notes in pairs of length and pitch
    notes = list()
    for i in range(len(pitches)):
        notes.append((length_key[int(lengths[i][0])], pitch_key[pitch_indices[i]]))

    return notes
