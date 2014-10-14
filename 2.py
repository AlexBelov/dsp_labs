import numpy as np
import matplotlib.pyplot as plt
import sys
from math import log

if (len(sys.argv) > 1) and (sys.argv[1].isdigit()) and ((log(int(sys.argv[1]))/log(2)).is_integer()):
  N = int(sys.argv[1])
else:
  N = 8

period = 2 * np.pi

class Config:
  fft = 0
  correlation = 0
  convolution = 0
  correlation_fft = 0
  convolution_fft = 0

def function(x):
  return np.sin(x) + np.cos(x)

def func_y(x):
  return np.cos(x)

def func_z(x):
  return np.sin(x)

def fft(a, dir):
  N = len(a)
  if N == 1 : return a

  a1 = [0] * (N / 2 + N % 2)
  a2 = [0] * (N / 2)

  i = 0
  while(i < N):
    if i % 2 == 0:
      a1[i / 2] = a[i]
    else:
      a2[i / 2] = a[i]
    i += 1
  b1 = fft(a1, dir)
  b2 = fft(a2, dir)

  wN = np.cos(2 * np.pi / N) + dir * np.sin(2 * np.pi / N) * 1j
  w = 1
  Config.fft += 6

  y = [0]*N
  j = 0
  while(j < N / 2):
    y[j] = b1[j] + b2[j] * w
    y[j + N /2] = b1[j] - b2[j] * w
    w *= wN
    j += 1
    Config.fft += 4

  return y

def convolution(x, func):
  y = function(x)
  z = func(x)

  N = len(y)

  res = [0] * N

  m = 0
  while (m < N):
    h = 0
    while (h < N):
      if (m - h >= 0):
        res[m] += y[h] * z[m - h]
      else:
        res[m] += y[h] * z[m - h + N]

      h += 1
      Config.convolution += 2

    res[m] /= N
    m += 1

  return res

def correlation(x, func):
  y = function(x)
  z = func(x)

  N = len(y)

  res = [0] * N

  m = 0
  while (m < N):
    h = 0
    while (h < N):
      if (m + h < N):
        res[m] += y[h] * z[m + h]
      else:
        res[m] += y[h] * z[m + h - N]

      h += 1
      Config.correlation += 2

    res[m] /= N
    m += 1

  return res

def convolution_fft(x, func):
  y = function(x)
  z = func(x)

  res_y = fft(y, 1)
  res_z = fft(z, 1)

  N = len(res_y)
  res_fft = [0] * N
  i = 0
  while (i < N):
    res_fft[i] = res_y[i] * res_z[i] / (N * N)
    i += 1
    Config.convolution_fft += 3

  res = fft(res_fft, -1)

  return res

def correlation_fft(x, func):
  y = function(x)
  z = func(x)

  res_y = fft(y, 1)
  res_z = fft(z, 1)

  N = len(res_y)
  i = 0
  while (i < N):
    res_y[i] = res_y[i].conjugate() / (N * N)
    i += 1
    Config.correlation_fft += 3

  res_fft = [0] * N
  i = 0
  while (i < N):
    res_fft[i] = res_y[i] * res_z[i]
    i += 1
    Config.correlation_fft += 1

  res = fft(res_fft, -1)
  return res

x = np.arange(0, period, period/N)
y = function(x)

corr = correlation(x, func_y)
corr_fft = correlation_fft(x, func_y)
conv = convolution(x, func_y)
conv_fft = convolution_fft(x, func_y)

corr1 = correlation(x, func_z)
corr_fft1 = correlation_fft(x, func_z)
conv1 = convolution(x, func_z)
conv_fft1 = convolution_fft(x, func_z)

print "Convolution: {}".format(Config.convolution)
print "Correlation: {}".format(Config.correlation)
print "Convolution FFT: {}".format(Config.convolution_fft + Config.fft/2)
print "Correlation FFT: {}".format(Config.correlation_fft + Config.fft/2)

fig, axes = plt.subplots(nrows=2, ncols=6, figsize=(6,6))

axes[0, 0].plot(x, y, 'r')
axes[0, 1].plot(x, func_y(x), 'brown')
axes[0, 2].plot(x, corr, 'g')
axes[0, 3].plot(x, np.real(corr_fft), 'blue')
axes[0, 4].plot(x, conv, 'black')
axes[0, 5].plot(x, np.real(conv_fft), 'pink')

axes[1, 0].plot(x, y, 'r')
axes[1, 1].plot(x, func_z(x), 'brown')
axes[1, 2].plot(x, corr1, 'g')
axes[1, 3].plot(x, np.real(corr_fft1), 'blue')
axes[1, 4].plot(x, conv1, 'black')
axes[1, 5].plot(x, np.real(conv_fft1), 'pink')

plt.show()
