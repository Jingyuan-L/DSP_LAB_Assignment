% read wav file
[x, Fs] = audioread('16bits_sin_3channels.wav'); 
whos
Fs

% Plot waveform
figure(1)
clf
plot(x)
xlabel('Time (sample)')
xlim(1 + [0 64])

