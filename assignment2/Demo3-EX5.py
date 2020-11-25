# filter_16.py
#
# Implement the second-order recursive difference equation
# y(n) = b0 x(n) + b1 x(n-1) + b2 x(n-2) - a1 y(n-1) - a2 y(n-2)

# 16 bit/sample

from math import cos, pi
import pyaudio
import struct


# Fs : Sampling frequency (samples/second)
Fs = 8000
# Also try other values of 'Fs'. What happens? Why?

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Difference equation coefficients
a1 = -1.9
a2 = 0.998
b0 = 1
b1 = -1.45
b2 = 0

# Initialization
y1 = 0.0
y2 = 0.0
x1 = 1.0
y = []
gain = 5400.0
# Also try other values of 'gain'. What is the effect?
# gain = 20000.0

# Create an audio object and open an audio stream for output
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                rate = Fs,
                input = False,
                output = True)

# paInt16 is 16 bits/sample

# Run difference equation
for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y0 = b0 * x0 + b1 * x1 - a1 * y1 - a2 * y2
    # x0 = 1 / b0 * (y0 + a1 * y1 + a2 * y2 - b1 * x1)
    y.append(y0)

    # Delays
    y2 = y1
    y1 = y0
    x1 = x0

    # Output
    output_value = gain * y0
    output_string = struct.pack('h', int(output_value))   # 'h' for 16 bits
    stream.write(output_string)

print("* Finished *")
print(min(abs((2**15-1))/max(y), abs(2**15/min(y))))
# gain < abs(min((2^15-1)/max(y), 2**15/min(y)))

stream.stop_stream()
stream.close()
p.terminate()
