import numpy as np
import matplotlib.pyplot as plt
import cmath as cmath

N = 64
period = 2 * np.pi

def function(x):
  return np.cos(x) + np.sin(x)

def dft(x, dir):
  i = 0
  N = len(x)
  y = [0]*N
  for k in range(0, N):
    for m in range(0, N):
      y[k] += x[m] * np.exp(-dir * 2j * np.pi * k * m / N)
      i += 1
    if dir == 1:
      y[k] /= N
  return y

# def fft(a, dir):
#   N = len(a)
#   if N == 1 : return a

#   a1 = [0] * (N / 2 + N % 2)
#   a2 = [0] * (N / 2)

#   i = 0
#   while(i < N):
#       if i % 2 == 0:
#         a1[i / 2] = a[i]
#       else:
#         a2[i / 2] = a[i]
#       i += 1
#   b1 = fft(a1, dir)
#   b2 = fft(a2, dir)

#   wN = np.cos(2 * np.pi / N) + dir * np.sin(2 * np.pi / N) * 1j
#   w = 1

#   y = [0]*N
#   j = 0
#   while(j < N / 2):
#       y[j] = b1[j] + b2[j] * w
#       y[j + N /2] = b1[j] - b2[j] * w
#       w *= wN
#       j += 1

#   return y

def W(n, N, dir):
  return np.exp(-1j * dir * 2 * np.pi * n/N)

def fft(x, dir):
  N = len(x)
  if N <= 1:
    return x
  even = fft(x[0::2], dir)
  odd = fft(x[1::2], dir)
  return [even[n] + W(n, N, dir) * odd[n] for n in xrange(N/2)] + \
         [even[n] - W(n, N, dir) * odd[n] for n in xrange(N/2)]

x = np.arange(0, period, period/N)

y = function(x)
y_dft = dft(y, 1)
dft_abs = map(abs, y_dft)
dft_phase = map(cmath.phase, y_dft)
y_idft = np.real(dft(y_dft, -1))

y_fft = fft(y, 1)
fft_abs = map(abs, y_fft)
fft_phase = map(cmath.phase, y_fft)
y_ifft = np.real(np.divide(fft(y_fft, -1),N))

# y_fft = np.fft.fft(y)
# fft_abs = map(abs, y_fft)
# fft_phase = map(cmath.phase, y_fft)
# y_ifft = np.real(np.fft.ifft(y_fft))

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(6,6))

axes[0,0].plot(x, y, 'r')
axes[0,1].plot(x, dft_abs, 'g')
axes[0,2].plot(x, dft_phase, 'blue')
axes[0,3].plot(x, y_idft, 'black')

axes[1,0].plot(x, y, 'r')
axes[1,1].plot(x, fft_abs, 'g')
axes[1,2].plot(x, fft_phase, 'blue')
axes[1,3].plot(x, y_ifft, 'black')

plt.show()
