import pyaudio, struct
import numpy as np
import random
from scipy import signal
from math import sin, cos, pi

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)
Fs = 8000
# Karplus-Strong paramters
K = 0.93
N = 60

# Define input signal
T = 2.0 # time duration (seconds)

# Buffer to store past signal values. Initialize to zero.
buffer = np.random.normal(0, 1, N)   # list of zeros

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = Fs,
                input       = False,
                output      = True )

print('* Start')

# compute ouput of filter
for i in range(N + int(T*Fs)):

    y = K * 0.5 * (buffer[i%N] + buffer[(i+1)%N])
    buffer[i%N] = y


    y = np.clip(int(y * 2**16), -MAXVALUE, MAXVALUE)
    binary_data = struct.pack('h', y);  # Convert to binary binary data
    stream.write(binary_data)


print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()