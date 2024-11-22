from midiutil import MIDIFile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk
import ipywidgets as widgets

# Defining simple scales 
major = (0, 2, 4, 5, 7, 9, 11, 12)
minor_harm = (0, 2, 3, 5, 7, 8, 11, 12)
minor_nat = (0, 2, 3, 5, 7, 8, 10, 12)
all_scales = (major, minor_harm, minor_nat)

scale_index = {
  "major": 0,
  "minor-harmonic" : 1,
  "minor-natural": 2
} 

scales=("major", "minor-harmonic", "minor-natural")

# Define basic chord intervals 
maj_135 = (0, 4, 7)
min_135 = (0, 3, 7)

# Defining octaves as is in MIDI format 
middle_octave = 4 
all_octave = np.arange(0,10,1)

# Defining notes to index via dictionary 

notes_to_index = {
  "C": 0,
  "C#/Db" : 1,
  "D": 2,
  "D#/Eb": 3,
  "E": 4,
  "F": 5,
  "F#/Gb": 6,
  "G": 7,
  "G#/Ab": 8,
  "A": 9,
  "A#/Bb": 10,
  "B": 11,
}

notes = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab", "A","A#/Bb","B"]

len_oct = len(notes)

num_octaves = 10 


# Specifying some defaults 

time = 0
track=0
notes_per_quarter = 8  
clocks_per_tick = 24
duration = 1 

# Defining slides/widgets 
## Setting key
des_note= widgets.Label('What key do you want your piece to be in?')
def_note = widgets.Dropdown(
    options=notes,
    layout=widgets.Layout(
        width='300px',           # Set the width of the slider
        border='2px solid lightblue'  # Border around the widget
    )
)
vert_note = widgets.VBox([des_note, def_note])

des_scale= widgets.Label('What scale do you want to map to?')
def_scale = widgets.Dropdown(
    options=scales, 
    layout=widgets.Layout(
        width='300px',           # Set the width of the slider
        border='2px solid lightblue'  # Border around the widget
    )
)
vert_scale= widgets.VBox([des_scale, def_scale])

des_octave= widgets.Label('Which octave do you want to assign your notes to? \n Middle C is in the 4th')
def_octave = widgets.Dropdown(
    options=np.arange(0,num_octaves,1),
    layout=widgets.Layout(
        width='300px',           # Set the width of the slider
        border='2px solid lightblue'  # Border around the widget
    )
)
vert_octave= widgets.VBox([des_octave, def_octave])


## MIDI setup
# des_track_num = widgets.Label('What is the track number?')
# def_track_num = widgets.IntText(
#     value=1,
#     disabled=False,
#     layout=widgets.Layout(width='300px'),
#     style={'description_width': 'initial'} 
# )
# vert_track = widgets.VBox([des_track_num, def_track_num])

des_channel = widgets.Label('What is the MIDI channel? \n (If unknown set as 0)')
def_channel = widgets.IntSlider(
    value=0,
    min=0,
    max=15,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    layout=widgets.Layout(width='300px', border='2px solid lightblue' ),
    style={'description_width': 'initial'} 
)
vert_channel = widgets.VBox([des_channel, def_channel])

des_time = widgets.Label('Define time for track ( in BPM):')
def_time = widgets.FloatText(
    value=0,
    disabled=False,
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_time = widgets.VBox([des_time, def_time])

des_tempo = widgets.Label('What is the tempo for the track?')
def_tempo = widgets.IntSlider(
    value=120,
    min=0,
    max=270,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_tempo = widgets.VBox([des_tempo, def_tempo])

des_ticks = widgets.Label('How many ticks per quarter note?')
def_ticks_per_quarter_note = widgets.Dropdown(
    value=1,
    options=[1,2,3,4],
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_ticks = widgets.VBox([des_ticks, def_ticks_per_quarter_note])

# des_note = widgets.Label('Number of 32nd note in a quarter note? \n (This is by default 8)')
# def_notes_per_quarter = widgets.IntSlider(
#     value=8,
#     min=1,
#     max=32,
#     step=1,
#     disabled=False,
#     continuous_update=False,
#     orientation='horizontal',
#     readout=True,
#     readout_format='d',
#     layout=widgets.Layout(width='300px'),
#     style={'description_width': 'initial'} 
# )
# vert_note = widgets.VBox([des_note, def_notes_per_quarter])

des_volume = widgets.Label('Volume of track')
def_volume = widgets.IntSlider(
    value=100,
    min=0,
    max=127,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_volume = widgets.VBox([des_volume, def_volume])

des_bpb = widgets.Label('What is the number of beats per bar')
def_bpb = widgets.Dropdown(
    options=[1,2,3,4],
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_bpb = widgets.VBox([des_bpb, def_bpb])

note_name_dictionary = {
  "Semi-brieve" : 1,
  "Minum": 2,
  "Crotchet" : 4,
  "Quaver": 8,
  "Semiquaver": 16
} 

note_names = [
  "Semi-brieve",
  "Minum",
  "Crotchet",
  "Quaver",
  "Semiquaver"
]
des_type_beat = widgets.Label('What type of note does each bar correspond to?')
def_type_beat = widgets.Dropdown(
    options=note_names,
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_type_beat  = widgets.VBox([des_type_beat, def_type_beat])


# track    = def_track_num.value

# Track file name 
des_name = widgets.Label('Name of your midi file:')

def_name = widgets.Textarea(
    value='Track_1',
    disabled=False,
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_name  = widgets.VBox([des_name, def_name])


# How often to get notes 
des_int = widgets.Label('How often to take a note from the data')
def_int = widgets.IntSlider(
    value=4,
    min=0,
    max=20,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    layout=widgets.Layout(width='300px', border='2px solid lightblue'),
    style={'description_width': 'initial'} 
)
vert_int = widgets.VBox([des_int, def_int])

