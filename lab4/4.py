import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

H =  [
        [
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ],
        [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ],
        [
            [1, -2, 1],
            [-2, 5, -2],
            [1, -2, 1]
        ],
        [
            [-0.1, -0.1, -0.1],
            [-0.1, 2, -0.1],
            [-0.1, -0.1, -0.1]
        ]
]

class F:
    min = 255
    max = 0

class G:
    min = 0
    max = 255

def brightness(current_pix):
    return 0.3*current_pix[0] + 0.59*current_pix[1] + 0.11*current_pix[2]

def linear_contrast(current_pix):
    result = []
    for clr in current_pix:
        result.append(int((clr - F.min)*(G.max - G.min)/(F.max - F.min) + G.min))
    return tuple(result)

def find_f(pix, width, height):
    for i in range(width):
        for j in range(height):
            current_brightness = brightness(pix[i,j])
            if current_brightness < F.min:
                F.min = current_brightness
            if current_brightness > F.max:
                F.max = current_brightness

def task_1(file_name, g_min, g_max):
    data_hist = []
    image = Image.open(file_name)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    find_f(pix, width, height)
    G.min = g_min
    G.max = g_max
    for i in range(width):
        for j in range(height):
            pix[i,j] = linear_contrast(pix[i,j])
            data_hist.append(brightness(pix[i,j]))
    return image, data_hist

def apply_filter_to_square(pix, H, i, j, width, height):
    result_r = 0
    result_b = 0
    result_g = 0

    min_k = i - 1
    max_k = i + 1
    min_l = j - 1
    max_l = j + 1

    if min_k < 0:
        min_k = 0
    if min_l < 0:
        min_l = 0
    if max_k > width:
        max_k = width
    if max_l > height:
        max_l = height

    for k in range(min_k, max_k):
        for l in range(min_l, max_l):
            current_pix = apply_filter_to_pixel(pix[k,l], H[k-i+1][l-j+1])
            result_r += current_pix[0]
            result_b += current_pix[1]
            result_g += current_pix[2]
    return (int(result_r),int(result_b),int(result_g))

def apply_filter_to_pixel(pix, H):
    result = []
    for clr in pix:
        res = int(clr*H)
        if res < 0:
            res = 0
        if res > 255:
            res = 255
        result.append(res)
    return tuple(result)

def task_2(file_name, H):
    data_hist = []
    image = Image.open(file_name)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for i in range(width):
        for j in range(height):
            pix[i,j] = apply_filter_to_square(pix, H, i, j, width, height)
            data_hist.append(brightness(pix[i,j]))
    return image, data_hist

file_name = "lenna.bmp"
image = Image.open(file_name)
image_1, data_hist_1 = task_1(file_name, 30, 150)
image_1.save("task1.jpg", "JPEG")
image_2, data_hist_2 = task_2(file_name, H[1])
image_2.save("task2.jpg", "JPEG")

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(6, 6))

axes[0, 0].imshow(image)
axes[0, 1].imshow(image_1)
axes[0, 2].hist(data_hist_1, 100, facecolor='black', alpha=0.5)

axes[1, 0].imshow(image)
axes[1, 1].imshow(image_2)
axes[1, 2].hist(data_hist_2, 100, facecolor='black', alpha=0.5)

plt.show()
