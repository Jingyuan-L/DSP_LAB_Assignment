# Mideterm Q1 - Jingyuan Li

import pyaudio, struct
from math import sin, cos, pi
import tkinter as Tk
import wave


def clip16(x):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return (x)


def fun_quit():
    global CONTINUE
    print('Good bye')
    CONTINUE = False

# Define Tkinter root
root = Tk.Tk()

# Define Tk variables
f1 = Tk.DoubleVar()
dur = Tk.DoubleVar()

# Initialize Tk variables
f1.set(200)   # f1 : frequency of sinusoid (Hz)
dur.set(1000) # dur : the duration of each note to be played (millisecond)

# Define widgets
S_freq = Tk.Scale(root, label = 'Frequency(Hz)', variable = f1, from_ = 100, to = 400, tickinterval = 100)
S_dur = Tk.Scale(root, label = 'Duration(millisecond)', variable = dur, from_ = 250, to = 2000)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_freq.pack(side = Tk.LEFT)
S_dur.pack(side = Tk.LEFT)


CONTINUE = True
BLOCKLEN = 1024  # Number of frames per block
WIDTH = 2  # Bytes per sample
CHANNELS = 1  # Number of channels
RATE = 8000  # Sampling rate in Hz (samples/second)

# Parameters
Ta = 0.5  # Decay time (seconds)

# Make second-order recursive filter

# Pole radius and angle
om1 = 2.0 * pi * float(f1.get()) / RATE
r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude

# Filter coefficients
a1 = -2 * r * cos(om1)
a2 = r ** 2
b0 = sin(om1)

y = BLOCKLEN * [0]

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format=PA_FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True)

# write the output to a wav file
wf = wave.open('Midterm_Q1_output.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)

print('* Start *')


# Loop through blocks
i = 0
while CONTINUE:

    root.update()
    om1 = 2.0 * pi * float(f1.get()) / RATE
    a1 = -2 * r * cos(om1)
    a2 = r ** 2
    b0 = sin(om1)

    # Do difference equation for block
    for n in range(BLOCKLEN):

        if i % ((dur.get()/1000)*RATE) == 0:
            x = 15000
        else:
            x = 0

        i = i + 1 if i < ((dur.get()/1000)*RATE) - 1 else 0

        y[n] = b0 * x - a1 * y[n - 1] - a2 * y[n - 2]
        y[n] = int(clip16(y[n]))

    # Convert numeric list to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *y);

    # Write binary data to audio output stream
    stream.write(output_bytes, BLOCKLEN)

    # Write data to wav file
    wf.writeframes(output_bytes)

print('* Finished *')

wf.close()
stream.stop_stream()
stream.close()
p.terminate()
