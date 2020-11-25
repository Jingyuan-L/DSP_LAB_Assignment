# echo_via_circular_buffer.py
# Reads a specified wave file (mono) and plays it with an echo.
# This implementation uses a circular buffer.

import pyaudio
import wave
import struct


def clip16(x):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return (x)


wavfile = 'Demo8_EX6_my_name.wav'
print('Input audio is from the microphone, and output signal is saved to %s.' % wavfile)

WIDTH = 2  # Number of bytes per sample
CHANNELS = 1  # mono
RATE = 16000  # Sampling rate (frames/second)
DURATION = 4  # duration of processing (seconds)

wf = wave.open(wavfile, 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)

TOTAL_FRAMES = DURATION * RATE  # N : Number of samples to process

print('The file has %d channel(s).' % CHANNELS)
print('The frame rate is %d frames/second.' % RATE)
print('The file has %d frames.' % TOTAL_FRAMES)
print('There are %d bytes per sample.' % WIDTH)

# Set parameters of delay system
b0 = 1.0  # direct-path gain
G = 0.8  # feed-forward gain
delay_sec = 0.05  # delay in seconds, 50 milliseconds   Try delay_sec = 0.02
N = int(RATE * delay_sec)  # delay in samples

print('The delay of %.3f seconds is %d samples.' % (delay_sec, N))

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN = N  # length of buffer
buffer = BUFFER_LEN * [0]  # list of zeros

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                output=True)

# Get first frame
input_bytes = stream.read(1)

# Initialize buffer index (circular index)
k = 0

print('* Start')

for _ in range(TOTAL_FRAMES):

    # # Get next frame
    # input_bytes = stream.read(1)

    # Convert binary data to number
    x0, = struct.unpack('h', input_bytes)

    # Compute output value
    # y(n) = b0 x(n) + G x(n-N)
    y0 = b0 * x0 + G * buffer[k]

    # Update buffer
    buffer[k] = x0

    # Increment buffer index
    k = k + 1
    if k >= BUFFER_LEN:
        # The index has reached the end of the buffer. Circle the index back to the front.
        k = 0

    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))

    # Write output value to audio stream
    stream.write(output_bytes)

    # Write data to wav file
    wf.writeframes(output_bytes)

    # Get next frame
    input_bytes = stream.read(1)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()
