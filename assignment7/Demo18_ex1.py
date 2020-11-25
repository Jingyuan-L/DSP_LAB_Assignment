# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
fk = [2**(k/12) * 440 for k in range(12)]  # Frequency (Hz)
# print(fk)

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om = [2.0 * pi * float(f)/RATE for f in fk]
# print(om)

# Filter coefficients (second-order IIR)
a = [[1, -2*r*cos(omi), r**2] for omi in om]
# print(a)
b = [[r*sin(omi)] for omi in om]
# print(b)
ORDER = 2   # filter order
states = np.zeros((12, ORDER))
x = np.zeros((12, BLOCKLEN))
y = np.zeros((12, BLOCKLEN))
# print(x)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
KEYPRESS = ''

def my_function(event):
    global CONTINUE
    global KEYPRESS
    print('You pressed ' + event.char)
    if event.char == 'q':
      print('Good bye')
      CONTINUE = False
    KEYPRESS = event.char

root = Tk.Tk()
root.bind("<Key>", my_function)

print('Press keys for sound.')
print('Press "q" to quit')
i = 0
while CONTINUE:
    root.update()

    if KEYPRESS != '' and CONTINUE:
        i =  ( ord(KEYPRESS) - ord('a') ) % 12
        print("The octave of this note is " + str(i+1) )
        # Some key (not 'q') was pressed
        x[i][0] = 10000.0

    [y[i], states[i]] = signal.lfilter(b[i], a[i], x[i], zi = states[i])

    x[i][0] = 0.0
    KEYPRESS = ''

    y[i] = np.clip(y[i].astype(int), -MAXVALUE, MAXVALUE)     # Clipping

    binary_data = struct.pack('h' * BLOCKLEN, *map(int, y[i]));    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
