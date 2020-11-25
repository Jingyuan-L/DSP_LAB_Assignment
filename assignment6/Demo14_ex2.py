# demo_filter_blocks_corrected.py
# Block filtering of a wave file, save the output to a wave file.
# Corrected version.

import pyaudio, wave, struct, math
import numpy as np
import scipy.signal
from matplotlib import pyplot


output_wavfile = 'Demo14_ex2_output.wav'

WIDTH = 2  # bytes per sample
CHANNELS = 1  # mono
RATE = 8000  # frames per second
BLOCKLEN = 1024  # block length in samples
DURATION = 5  # Duration in seconds
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)
K = int(DURATION * RATE / BLOCKLEN)  # Number of blocks

print('Block length: %d' % BLOCKLEN)
print('Number of blocks to read: %d' % K)
print('Duration of block in milliseconds: %.1f' % (1000.0 * BLOCKLEN / RATE))

output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081
b = [b0, 0.0, b2, 0.0, b4]

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829
a = [1.0, a1, a2, a3, a4]

# Set up plotting...

pyplot.ion()  # Turn on interactive mode
pyplot.figure(1)
[g1] = pyplot.plot([], [], 'blue')  # empty line of microphone input
[g2] = pyplot.plot([], [], 'red')  # empty line of filter output

binary_data = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)  # set x-axis limits
pyplot.xlabel('Time (n)')
pyplot.ylim(-10000, 10000)  # set y-axis limits
g1.set_xdata(binary_data)  # x-data of plot (discrete-time)
g2.set_xdata(binary_data)

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True )


for i in range(K):

    binary_data = stream.read(BLOCKLEN, exception_on_overflow=False)
    # convert binary data to numbers
    input_block = struct.unpack('h' * BLOCKLEN, binary_data)

    # filter
    [output_block, states] = scipy.signal.lfilter(b, a, input_block, zi = states)

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    # convert to integer
    output_block = output_block.astype(int)

    # Convert output value to binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(binary_data)

    # Write binary data to output wave file
    output_wf.writeframes(binary_data)

    # Update y-data of plot
    g1.set_ydata(input_block)
    g2.set_ydata(output_block)
    pyplot.pause(0.0001)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()

# Close wavefiles
output_wf.close()