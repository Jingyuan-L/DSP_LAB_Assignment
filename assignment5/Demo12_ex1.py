
import pyaudio
import struct
import math
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

# f0 = 0      # Normal audio
f0 = 400  # Modulation frequency (Hz)

BLOCKLEN = 1024  # Number of frames per block
WIDTH = 2  # Number of bytes per signal value
CHANNELS = 1  # mono
RATE = 32000  # Frame rate (frames/second)
RECORD_SECONDS = 10

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
pyplot.ylim(-10000, 10000)  # set y-axis limits


p = pyaudio.PyAudio()

stream = p.open(
    format=p.get_format_from_width(WIDTH),
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True)


# Initialize phase
om = 2 * math.pi * f0 / RATE
theta = 0

# Number of blocks to run for
num_blocks = int(RATE / BLOCKLEN * RECORD_SECONDS)

print('* Recording for %.3f seconds' % RECORD_SECONDS)

output_block = [0] * BLOCKLEN
# Start loop
for i in range(0, num_blocks):

    # Get frames from audio input stream
    # input_bytes = stream.read(BLOCKLEN)       # BLOCKLEN = number of frames read
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow=False)  # BLOCKLEN = number of frames read

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)

    # Go through block
    for n in range(0, BLOCKLEN):
        # No processing:
        # output_block[n] = input_tuple[n]
        # OR
        # Amplitude modulation:
        theta = theta + om
        output_block[n] = (clip16(int(input_tuple[n] * math.cos(theta))))

    # keep theta betwen -pi and pi
    while theta > math.pi:
        theta = theta - 2 * math.pi

    # Convert values to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio output stream
    stream.write(output_bytes)

    g1.set_ydata(input_tuple)  # Update y-data of plot
    g2.set_ydata(output_block)
    pyplot.pause(0.0001)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
