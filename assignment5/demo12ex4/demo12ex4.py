# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidally time-varying delay)
# Uses linear interpolation

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

#############################################################
# The new blocking way
wavfile = 'decay_cosine_mono.wav'
# wavfile = 'author.wav'
# wavfile = 'cosine_200_hz.wav'

print('Play the wave file: %s.' % wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties

BLOCKLEN = 64      # Number of frames per block
output_block = BLOCKLEN * [0]



RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 2
W = 0.2   # W = 0 for no effect

# f0 = 2; W = 0.2
om = 2 * math.pi * f0/RATE
theta = 0


# OR
# f0 = 2
# ratio = 2.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print(W)

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN =  1024          # Set buffer length.
buffer = BUFFER_LEN * [0]   # list of zeros

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)

print('The buffer is %d samples long.' % BUFFER_LEN)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )


num_blocks = int(LEN / BLOCKLEN )


print ('* Playing the output using blocking ...')
output_list_block = []
# Loop through wave file 
for n in range(0, num_blocks):

    # Get sample from wave file
    input_bytes = wf.readframes(BLOCKLEN)

    # Convert string to number
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
    
    #empty output block, will be filled by processed byte y, 64 in total
    output_block = BLOCKLEN * [0]
    
    for i in range(0, BLOCKLEN):
        
        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(math.floor(kr))
        frac = kr - kr_prev    # 0 <= frac < 1
        kr_next = kr_prev + 1
        if kr_next == BUFFER_LEN:
            kr_next = 0
        
        
        y = (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]
        
        output_block[i] = int(clip16(y))
        
        # Update buffer
        buffer[kw] = input_tuple[i]
        
        # Increment read index
        kr = kr + 1 + W * math.sin(theta)
        
        if kr >= BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr = kr - BUFFER_LEN
        
        
        # Increment write index    
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0
        
        
        theta = theta + om
        # keep theta betwen -pi and pi
        while theta > math.pi:
            theta = theta - 2*math.pi
        
        


    # Clip and convert output value to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)
    output_list_block.extend(output_block)

    # Write output to audio stream
    stream.write(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()

################################################################
# The original way
wavfile = 'decay_cosine_mono.wav'

# Open wave file
wf = wave.open(wavfile, 'rb')

# Read wave file properties
RATE = wf.getframerate()  # Frame rate (frames/second)
WIDTH = wf.getsampwidth()  # Number of bytes per sample
LEN = wf.getnframes()  # Signal length
CHANNELS = wf.getnchannels()  # Number of channels

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN = 1024  # Set buffer length.
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

print('* Playing the output not using blocking ...')
output_list_notblock = []
# Loop through wave file
for n in range(0, LEN):

    # Get sample from wave file
    input_bytes = wf.readframes(1)

    # Convert string to number
    x0, = struct.unpack('h', input_bytes)

    # Get previous and next buffer values (since kr is fractional)
    kr_prev = int(math.floor(kr))
    frac = kr - kr_prev  # 0 <= frac < 1
    kr_next = kr_prev + 1
    if kr_next == BUFFER_LEN:
        kr_next = 0

    # Compute output value using interpolation
    y0 = (1 - frac) * buffer[kr_prev] + frac * buffer[kr_next]

    # Update buffer
    buffer[kw] = x0

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

    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))
    output_list_notblock.append(int(clip16(y0)))

    # Write output to audio stream
    stream.write(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()


##############################################################
# Verify the outputs of old and new version are the same
FLAG = True
for i in range(1280):
    if output_list_block[i] != output_list_notblock[i]:
        FLAG = False
        break
if FLAG == True:
    print("Two version's outputs are exactly the same!")
else:
    print("Two version's outputs are NOT the same!")

