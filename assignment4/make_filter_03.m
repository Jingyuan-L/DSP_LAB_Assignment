%% make_filter_03.m 
% Filter twice for gradual rise time

%%

clc
clear

%% Difference equation
% y(n) = b0 x(n) - a1 y(n-1) - a2 y(n-2)

Fs = 8000;          % sampling frequency (sample/second)
F1 = 400;           % frequency (Hz)
f1 = F1/Fs          % normalized frequency (cycles/sample)
om1 = 2*pi * f1;    % normalized frequency (radians/sample)

Ta = 0.5;           % duration (seconds) [time till 1% amplitude]
r = 0.01^(1/(Ta*Fs))

a = [1 -2*r*cos(om1) r^2]   % recursive part
b = 1;                      % non-recursive part

%% Impulse response
% The amplitude envelope has the form r^n.

N = Fs;
n = 0:N;

imp = [1 zeros(1, N)];
h = filter(b, a, imp);

figure(1)
clf
plot(n/Fs, h)
title('Impulse response');
xlabel('Time (sec)')
zoom xon

%% Listen

soundsc(h, Fs)

%% Twice the filter

% Cascade of the same system twice:
a2 = conv(a, a)
b2 = conv(b, b)

h2 = filter(b2, a2, imp);

plot(n/Fs, h2)
title('Impulse response');
xlabel('Time (sec)')

% The amplitude envelope has the form n r^n.

% What is the peak amplitude in terms of f1 and r?


%% Listen

soundsc(h2, Fs)

%% Pole-zero plot
% Note: the poles double poles

zplane(b2, a2)
title('Pole-zero Plot')

%% Frequency response
% The frequency response has a peak at f1

[H2, om] = freqz(b2, a2);
f = om / (2*pi) * Fs;
plot(f, abs(H2))
title('Frequency response')
xlabel('Frequency (Hz)')
xlim([0 1000])
grid


