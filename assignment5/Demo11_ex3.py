import pyaudio
import struct
from matplotlib import pyplot


def clip16(x):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return (x)


WIDTH = 2  # bytes per sample
CHANNELS = 1  # mono
RATE = 8000  # frames per second
BLOCKLEN = 1024  # block length in samples
DURATION = 10  # Duration in seconds

K = int(DURATION * RATE / BLOCKLEN)  # Number of blocks

print('Block length: %d' % BLOCKLEN)
print('Number of blocks to read: %d' % K)
print('Duration of block in milliseconds: %.1f' % (1000.0 * BLOCKLEN / RATE))

# Difference equation coefficients
b0 = 0.008442692929081
b2 = -0.016885385858161
b4 = 0.008442692929081

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 = 4.942669993770672
a3 = -3.114402101627517
a4 = 0.757546944478829

# Initialization
x1 = 0.0
x2 = 0.0
x3 = 0.0
x4 = 0.0
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0

# Set up plotting...

pyplot.ion()  # Turn on interactive mode
pyplot.figure(1)
[g1] = pyplot.plot([], [], 'blue')  # empty line of microphone input
[g2] = pyplot.plot([], [], 'red')  # empty line of filter output

n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)  # set x-axis limits
pyplot.xlabel('Time (n)')
g1.set_xdata(n)  # x-data of plot (discrete-time)
g2.set_xdata(n)

# --- Time axis in units of milliseconds ---
# t = [n*1000/float(RATE) for n in range(BLOCKLEN)]
# pyplot.xlim(0, 1000.0 * BLOCKLEN/RATE)         # set x-axis limits
# pyplot.xlabel('Time (msec)')
# g1.set_xdata(t)                   # x-data of plot (time)

pyplot.ylim(-10000, 10000)  # set y-axis limits

# Open the audio stream

p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(
    format= PA_FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    # output_device_index = 1
    )

# Read microphone, plot audio signal, and filtered signal
print('* Start')
for i in range(K):
    # Read audio input stream
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)

    signal_block = struct.unpack('h' * BLOCKLEN, input_bytes)  # Convert

    input_values = list(signal_block)
    # print(signal_block)

    # use butterworth bandpass flter to flter the input audio from the microphone
    output_block = []
    for j in range(BLOCKLEN):

        # Set input to difference equation
        x0 = input_values[j]

        # Difference equation
        y0 = b0 * x0 + b2 * x2 + b4 * x4 - a1 * y1 - a2 * y2 - a3 * y3 - a4 * y4
        # y(n) = b0 x(n) + b2 x(n-2) + b4 x(n-4) - a1 y(n-1) - a2 y(n-2) - a3 y(n-3) - a4 y(n-4)

        # Delays
        x4 = x3
        x3 = x2
        x2 = x1
        x1 = x0
        y4 = y3
        y3 = y2
        y2 = y1
        y1 = y0

        # Compute output value
        output_value = int(clip16(y0))  # Integer in allowed range
        output_block.append(output_value)
        # Convert output value to binary data
        output_bytes = struct.pack('h', output_value)
        # Write binary data to audio stream
        stream.write(output_bytes)

    g1.set_ydata(signal_block)  # Update y-data of plot
    g2.set_ydata(output_block)
    pyplot.pause(0.0001)

stream.stop_stream()
stream.close()
p.terminate()

pyplot.ioff()  # Turn off interactive mode
pyplot.show()  # Keep plot showing at end of program

pyplot.close()
print('* Finished')
