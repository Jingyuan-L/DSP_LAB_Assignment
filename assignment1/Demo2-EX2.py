import wave

wf = wave.open('hello.wav')
channel = wf.getnchannels()  # number of channels
framerate = wf.getframerate()  # frame rate (number of frames per second)
frames = wf.getnframes()  # total number of frames (length of signal)
width = wf.getsampwidth()  # number of bytes per sample
wf.close()
print(channel, framerate, frames, width)

# For my 16-bits wav file, the width returned by getsampwidth() is 2.
