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

def vibrato_interpolation(x0, kr, kw):
    # Get previous and next buffer values (since kr is fractional)
    kr_prev = int(math.floor(kr))
    frac = kr - kr_prev  # 0 <= frac < 1
    kr_next = kr_prev + 1
    if kr_next == BUFFER_LEN:
        kr_next = 0

    # Compute output value using interpolation
    y0 = (1 - frac) * buffer[kr_prev] + frac * buffer[kr_next]
    # print(y0, kr_prev, kr_next, frac)

    # Update buffer
    buffer[kw] = x0
    # print(x0)

    # Increment read index
    kr = kr + 1 + W * math.sin(2 * math.pi * f0 * n / RATE)
    # Note: kr is fractional (not integer!)

    # Ensure that 0 <= kr < BUFFER_LEN
    if kr >= BUFFER_LEN:
        # End of buffer. Circle back to front.
        kr = kr - BUFFER_LEN

    # Increment write index
    kw = kw + 1
    if kw == BUFFER_LEN:
        # End of buffer. Circle back to front.
        kw = 0

    # print(kr, kw)
    # Clip and convert output value to binary data
    output_value = int(clip16(y0))

    return kr, kw, output_value


wavfile = 'decay_cosine_mono.wav'
# wavfile = 'author.wav'
# wavfile = 'cosine_200_hz.wav'

print('Play the wave file: %s.' % wavfile)


# Open wave file
wf = wave.open(wavfile, 'rb')

# Read wave file properties
RATE = wf.getframerate()  # Frame rate (frames/second)
WIDTH = wf.getsampwidth()  # Number of bytes per sample
LEN = wf.getnframes()  # Signal length
CHANNELS = wf.getnchannels()  # Number of channels

print('The file has %d channel(s).' % CHANNELS)
print('The file has %d frames/second.' % RATE)
print('The file has %d frames.' % LEN)
print('The file has %d bytes per sample.' % WIDTH)

# Vibrato parameters
f0 = 2
W = 0.2  # W = 0 for no effect

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN = 1024  # Set buffer length.
buffer = BUFFER_LEN * [0]  # list of zeros

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)

print('The buffer is %d samples long.' % BUFFER_LEN)


# The original play_vibrato_interpolation.py file, does not use blocking
# Store the output data in output_single list
output_single = []
# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=False,
                output=True)

print('* Playing the old version...')

# Loop through wave file
for n in range(0, LEN):

    # Get sample from wave file
    input_bytes = wf.readframes(1)

    # Convert string to number
    x0, = struct.unpack('h', input_bytes)

    kr, kw, output_value = vibrato_interpolation(x0, kr, kw)

    output_bytes = struct.pack('h', output_value)
    output_single.append(output_value)

    # Write output to audio stream
    stream.write(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()


# The new version, use block processing
# Store the output data in output_blocking list
output_blocking = []
# Open wave file
wf = wave.open(wavfile, 'rb')

buffer = BUFFER_LEN * [0]  # list of zeros

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=False,
                output=True)

BLOCKLEN = 64      # Number of frames per block

# Create block (initialize to zero)
output_block = BLOCKLEN * [0]

# Number of blocks in wave file
num_blocks = int(math.floor(LEN/BLOCKLEN))

print('* Playing the new version using block processing...')

# Loop through wave file
for i in range(0, num_blocks):

    # Get block of samples from wave file
    input_bytes = wf.readframes(BLOCKLEN)     # BLOCKLEN = number of frames to read

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)

    # Go through block
    for n in range(0, BLOCKLEN):
        x0 = input_tuple[n]
        kr, kw, output_value = vibrato_interpolation(x0, kr, kw)
        output_block[n] = output_value
        output_blocking.append(output_value)
        # print(kr, kw)

    # Convert values to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio output stream
    stream.write(output_bytes)

print('* Finished *')

stream.stop_stream()
stream.close()
p.terminate()

# Close wavefiles
wf.close()

# Verify the outputs of old and new version are the same
FLAG = True
for i in range(1280):
    if output_single[i] != output_blocking[i]:
        FLAG = False
        break
if FLAG == True:
    print("Two version's outputs are the same!")
else:
    print("Two version's outputs are NOT the same!")

