import numpy as np
import matplotlib.pyplot as plt
import sys
from math import log

if (len(sys.argv) > 1) and (sys.argv[1].isdigit()) and ((log(int(sys.argv[1]))/log(2)).is_integer()):
  N = int(sys.argv[1])
else:
  N = 8

period = 2 * np.pi

def function(x):
  return (np.sin(x) + np.cos(x))

def FWT(x, dir):
  N = len(x)
  if N <= 1:
    return x

  left = [0] * (N / 2)
  right = [0] * (N / 2)
  i = 0
  while (i < N / 2):
    left[i] = x[i] + x[i + (N / 2)]
    right[i] = x[i] - x[i + (N / 2)]
    i += 1

  b_l = FWT(left, dir)
  b_r = FWT(right, dir)

  res = [0] * N

  i = 0
  if (dir == 1):
    while (i < N / 2):
      res[i] = b_l[i] / 2
      res[i + (N / 2)] = b_r[i] / 2
      i += 1

  else:
    while (i < N / 2):
      res[i] = b_l[i]
      res[i + (N / 2)] = b_r[i]
      i += 1

  return res

x = np.arange(0, period, period/N)
y = function(x)

fwt = FWT(y, 1)
rev_fwt = FWT(fwt, -1)

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(6, 6))

axes[0].plot(x, y, 'r')
axes[1].plot(x, fwt, 'g')
axes[2].plot(x, rev_fwt, 'blue')

plt.show()
