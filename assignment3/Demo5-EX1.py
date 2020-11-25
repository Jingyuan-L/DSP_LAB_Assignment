# play_wave_mono.py

import pyaudio
import wave
import struct
import math


def clip16(x):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return (x)


gain = 1.0
# Try another value of gain, such as 10, 100, 1000
# gain = 10

# Choose files with different channel number
# wavefile = 'author.wav'
# wavefile = 'sin01_mono.wav'
wavefile = 'sin01_stereo.wav'

print('Play the wave file %s.' % wavefile)

# Open wave file
wf = wave.open(wavefile, 'rb')

# Read the wave file properties
num_channels = wf.getnchannels()  # Number of channels
RATE = wf.getframerate()  # Sampling rate (frames/second)
signal_length = wf.getnframes()  # Signal length
width = wf.getsampwidth()  # Number of bytes per sample

print('The file has %d channel(s).' % num_channels)
print('The frame rate is %d frames/second.' % RATE)
print('The file has %d frames.' % signal_length)
print('There are %d bytes per sample.' % width)

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format=pyaudio.paInt16,
    channels=num_channels,
    rate=RATE,
    input=False,
    output=True)

# Get first frame
input_bytes = wf.readframes(1)

if num_channels == 1:
    print('Output the mono file')
    while len(input_bytes) > 0:
        # Convert binary data to number
        input_tuple = struct.unpack('h', input_bytes)  # One-element tuple (unpack produces a tuple)
        input_value = input_tuple[0]  # Number
        # Compute output value
        output_value = int(clip16(gain * input_value))  # Integer in allowed range
        # Convert output value to binary data
        output_bytes = struct.pack('h', output_value)

        # Write binary data to audio stream
        stream.write(output_bytes)
        # Get next frame
        input_bytes = wf.readframes(1)

elif num_channels == 2:
    print('Output the stereo file')
    while len(input_bytes) > 0:
        # Convert binary data to numbers
        input_tuple = struct.unpack('hh', input_bytes)  # produces a two-element tuple
        # Compute output values
        output_value0 = int(clip16(gain * input_tuple[0]))
        output_value1 = int(clip16(gain * input_tuple[1]))
        # Convert output value to binary data
        output_bytes = struct.pack('hh', output_value0, output_value1)

        # Write binary data to audio stream
        stream.write(output_bytes)
        # Get next frame
        input_bytes = wf.readframes(1)

print('* Finished *')

stream.stop_stream()
stream.close()
p.terminate()


