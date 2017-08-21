This is my control script emulating some of the functions of the Akai APC 40 
on an Akai MPD 26. 

The hope is that with a fairly basic understanding of python and how control 
scripts in Live work that anyone will be able to adapt or expand upon this script
to bring these functions to any midi controller.

If you want to emulate my workflow on my Akai MPD you will need to set it up the following way: 

PAD BANK A: 
Channel 1A

48 49 50 51
44 45 46 47
40 41 42 43
36 37 38 39

PAD BANK B: 
Channel 2A

64 65 66 67 
60 61 62 63
56 57 68 69
52 53 54 55

PAD BANK C: 
Channel 2A

80 81 82 83
76 77 78 79
72 73 74 75 
68 69 70 71

PAD BANK D: 
Channel 2A 

48 49 50 51
44 45 46 47
40 41 42 43
36 37 38 39

FADERS: 
Channel 2A 

12 13 14 15 03 07

KNOBS: 
Channel 2A 

02 06
01 05 
00 04


The setup is fairly logical, I have all my Live functions on MIDI channel 2A, all my notes that I 
want Live to play on an instrument are on channel 1A. That way, I have access to all 0-127 midi values 
to send to Live as notes. 

For the above setup then: 

BANK A = first 16 pads in a drum rack 
BANK B = corresponds to the red launch grid
BANK C = first row is track select, second row device select/control, third row is scene launch, fourth is track stop
BANK D = first row is red box navigation, the next three rows are then mute, solo and arm for each track 

First four faders are volume for the red box. 

The last two faders and the knobs correspond to the 8 macro controls in a device/instrument rack. 

Enjoy! 



