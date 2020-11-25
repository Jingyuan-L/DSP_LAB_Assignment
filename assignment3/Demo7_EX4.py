
import pyaudio
import struct
import math
import wave

def clip16(x):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return (x)


WIDTH       = 2         # Number of bytes per sample
CHANNELS    = 1         # mono
RATE        = 16000     # Sampling rate (frames/second)
DURATION    = 6         # duration of processing (seconds)

wf = wave.open('Demo7_EX4_my_talking.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)

N = DURATION * RATE     # N : Number of samples to process

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)

print('* Start')

for n in range(0, N):

    # Get one frame from audio input (microphone)
    input_bytes = stream.read(1)
    # If you get run-time time input overflow errors, try:
    # input_bytes = stream.read(1, exception_on_overflow = False)

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h', input_bytes)

    # Convert one-element tuple to number
    x0 = input_tuple[0]

    # Amplitude Modulation
    # y(t) = x(t) cos(2*pi*f0*t)
    # f0 = 400Hz
    y0 = x0 * math.cos(2 * math.pi * 400 * n/RATE)

    # Compute output value
    output_value = int(clip16(10*y0))    # Number

    # output_value = int(clip16(x0))   # Bypass filter (listen to input directly)

    # Convert output value to binary data
    output_bytes = struct.pack('h', output_value)

    # Write binary data to audio stream
    stream.write(output_bytes)

    # Write data to wav file
    wf.writeframes(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()