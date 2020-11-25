# Midterm Q2 - Jingyuan Li

import pyaudio, struct
import wave
import numpy as np


def clip16(x):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return (x)


BLOCKLEN = 4096  # Number of frames per block
WIDTH = 2  # Bytes per sample
CHANNELS = 1  # Number of channels
RATE = 8000  # Sampling rate in Hz (samples/second)
RECORD_SECONDS = 5

# Open the audio input and output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format=PA_FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True)

# write the input and output to wav files
wf_in = wave.open('Midterm_Q2_input.wav', 'w')
wf_in.setnchannels(CHANNELS)
wf_in.setsampwidth(WIDTH)
wf_in.setframerate(RATE)

# write the input and output to wav files
wf_out = wave.open('Midterm_Q2_output.wav', 'w')
wf_out.setnchannels(CHANNELS)
wf_out.setsampwidth(WIDTH)
wf_out.setframerate(RATE)

# read impulse response file
wf_imp = wave.open('impulse_response_8kHz.wav', 'r')
signal_length   = wf_imp.getnframes()       # Signal length
print('The impulse response file has %d frames.' % signal_length)

L = signal_length + BLOCKLEN - 1

# Number of blocks to run for
num_blocks = int(RATE / BLOCKLEN * RECORD_SECONDS)

print('* Start *')


overlap_add = []
h_bytes = wf_imp.readframes(signal_length)
h_tuple = struct.unpack('h' * signal_length, h_bytes)
H = np.fft.fft(h_tuple, L)

# Loop through blocks
for i in range(0, num_blocks):

    input_bytes = stream.read(BLOCKLEN, exception_on_overflow=False)
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)

    wf_in.writeframes(input_bytes)

    y = np.convolve(input_tuple, h_tuple)
    for j in range(len(y)):
        y[j] = int(clip16(y[j]))
    output_bytes = struct.pack('h' * BLOCKLEN, *y[:BLOCKLEN])

    wf_out.writeframes(output_bytes)
    stream.write(output_bytes, BLOCKLEN)


print('* Finished *')
wf_in.close()
wf_out.close()
wf_imp.close()
stream.stop_stream()
stream.close()