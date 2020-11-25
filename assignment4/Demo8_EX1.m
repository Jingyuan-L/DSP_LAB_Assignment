
clc
clear

info = audioinfo('author.wav')
[x, Fs] = audioread('author.wav');
delay_sec = 0.05;
N = 16000 * delay_sec;

% Difference equation
% y(n) = b0 x(n) + G x(n - N)
G = 0.8;
a = 1;      
b = [1 zeros(1,N-1) G];              
r = 0.9;            % pole radius

% Pole-zero plot
figure(1)
zplane(b, a)
title('Pole-zero plot')

