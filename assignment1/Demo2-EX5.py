from struct import pack
from math import sin, pi
import wave
Fs = 8000
# Write a mono wave file
wf = wave.open('8bits_sin_wav.wav', 'w')
wf.setnchannels(1)
wf.setsampwidth(1)
wf.setframerate(Fs)
A = 2 ** 7 - 1
f = 261.6
N = int (0.5 * Fs)
for n in range(N):
    x = A * sin(2 * pi * f / Fs * n)
    byte_string = pack('B', int(x + 128))
    wf.writeframes(byte_string)
# print(wf.getframerate())
wf.close()
