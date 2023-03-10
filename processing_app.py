#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:01:24 2023

@author: cobeliu
"""

import bm3d
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import img_as_float, img_as_ubyte
from skimage.filters import sobel, unsharp_mask
from skimage.restoration import denoise_tv_chambolle, denoise_nl_means
import os

### Functions to perform their process on img

def bilateral(in_img):
    try:
        kernel_size = int(input('Kernel Size (int): '))
        sigma_color_int = int(input('Sigma Color Int (spatial weighting) (0 to 255): '))
        sigma_space_int = int(input('Sigma Space Int (range weighting) (0 to 255): '))
        out_img = cv2.bilateralFilter(in_img, kernel_size, sigma_color_int, sigma_space_int, borderType = cv2.BORDER_CONSTANT)
        return out_img
    except:
        print('ERROR')
        
def bm3d_func(in_img):
    in_img = img_as_float(in_img)
    try: 
        sigma_psd_input = float(input('Noise Standard Deviation (0 to 1): '))
        stage = ''
        while not (stage == 'A' or stage == 'H'):
            stage = input('All Stages (A) or Hard Thresholding (H): ')
            if stage == 'A':
                out_img = img_as_ubyte(bm3d.bm3d(in_img, sigma_psd = sigma_psd_input, stage_arg = bm3d.BM3DStages.ALL_STAGES))
            elif stage == 'H':
                out_img = img_as_ubyte(bm3d.bm3d(in_img, sigma_psd = sigma_psd_input, stage_arg = bm3d.BM3DStages.HARD_THRESHOLDING))
        return out_img
    except:
        print('ERROR')
        
def canny(in_img):
    try:    
        lower_threshold = int(input('Lower Threshold (0 to 255): '))
        upper_threshold = int(input('Upper Threshold (0 to 255): '))
        in_img = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
        out_img = cv2.Canny(in_img, lower_threshold, upper_threshold)
        return out_img
    except:
        print('ERROR')

def channel_isolation(in_img):
    channel = -1
    while not (channel == 0 or channel == 1 or channel == 2):
        try: 
            channel = int(input('Channel (blue(0), green(1), red(2)): '))
        except:
            print('Channel must be int 0, 1, or 2')
    out_img = in_img[:, :, channel]
    return out_img

def gaussian(in_img):
    try:
        kernel_size = int(input('Kernel Size (int): '))
        out_img = cv2.GaussianBlur(in_img, (kernel_size, kernel_size), 0, borderType = cv2.BORDER_CONSTANT)
        return out_img
    except:
        print('ERROR')

def gray(in_img):
    out_img = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
    return out_img

def median(in_img):
    try:
        kernel_size = int(input('Kernel Size (int): '))
        out_img = cv2.medianBlur(in_img, kernel_size)
        return out_img
    except:
        print('ERROR')
        
def non_local_means(in_img):
    try:
        in_img = img_as_float(in_img)
        
        h_input = float(input('Filter Strength (0 to 1): '))
        patch_size_input = int(input('Patch Size (num of pixels) (should be odd) (e.g. 7): '))
        patch_distance_input = int(input('Patch Distance (num of pixels) (should be odd) (e.g. 21): '))
        out_img = denoise_nl_means(in_img, h=h_input, fast_mode=True, patch_size=patch_size_input, patch_distance=patch_distance_input, channel_axis=True)
        out_img = img_as_ubyte(out_img)
        return out_img
    except:
        print('ERROR')
        
def rescale(in_img):
    try:
        fx_input = float(input('x Scale: '))
        fy_input = float(input('y Scale: '))
        out_img = cv2.resize(in_img, None, fx = fx_input, fy = fy_input, interpolation = cv2.INTER_CUBIC)
        return out_img
    except:
        print('ERROR')

def sobel_func(in_img):
    in_img = gray(in_img)
    out_img = sobel(in_img)
    return out_img

def total_variation(in_img):
    try:
        in_img = img_as_float(in_img)
        
        weight_input = float(input('Weight (0 to 1): '))
        eps_input = float(input('Passable Error (e.g. 0.0002): '))
        n_inter_max_input = int(input('Maximum # of Iterations: '))
        
        correct_input = False
        multichannel_input = False
        while correct_input == False:
            multichannel = input('Multichannel (y or n): ')
            if multichannel == 'y':
                multichannel_input = True
                correct_input = True
            elif multichannel == 'n':
                multichannel_input = False
                correct_input = True
        
        out_img = denoise_tv_chambolle(in_img, weight = weight_input, eps = eps_input, max_num_iter = n_inter_max_input, channel_axis = multichannel_input)
        out_img = img_as_ubyte(out_img)
        return out_img
    except: 
        print('ERROR')
        
def unsharp_mask_func(in_img):
    try:
        amount_input = float(input('Mask Multiplication Factor (e.g. 2): '))
        kernel_size = int(input('Kernel Size (int): '))
        out_img = img_as_ubyte(unsharp_mask(in_img, radius=kernel_size, amount=amount_input))
        return out_img
    except:
        print('ERROR')

processes = ['bilateral', 'bm3d', 'canny', 'channel isolation', 'gaussian', 'gray', 'median', 'non-local means', 'rescale', 'sobel', 'total variation', 'unsharp mask']
image_list = os.listdir('/Users/cobeliu/ImageProcessing/images')

process = ''
image = ''

### Get image and process from user

while not image in image_list:
    image = input('Image (input o to see options): ')
    if image == 'o':
        for item in image_list:
            print(item)
    
while not process in processes:
    process = input('Process (input o to see options): ')
    if process == 'o':
        for item in processes:
            print(item)

img = cv2.imread('images/' + image)

### process image

processed_img = []
if process == 'bilateral':
    processed_img = bilateral(img)
elif process == 'bm3d':
    processed_img = bm3d_func(img)
elif process == 'canny':
    processed_img = canny(img)
elif process == 'channel isolation':
    processed_img = channel_isolation(img)
elif process == 'gaussian':
    processed_img = gaussian(img)
elif process == 'gray':
    processed_img = gray(img)
elif process == 'median':
    processed_img = median(img)
elif process == 'non-local means':
    processed_img = non_local_means(img)
elif process == 'rescale':
    processed_img = rescale(img)
elif process == 'sobel':
    processed_img = sobel_func(img)
elif process == 'total variation':
    processed_img = total_variation(img)
elif process == 'unsharp mask':
    processed_img = unsharp_mask_func(img)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
if img.shape == processed_img.shape:
    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)

### show image

fig = plt.figure(figsize = (10, 10))

ax1 = fig.add_subplot(3, 3, 1)
ax1.imshow(img)
ax1.title.set_text('Original Image')

ax2 = fig.add_subplot(3, 3, 2)
ax2.imshow(processed_img)
ax2.title.set_text('Processed Image')

plt.show

## save image if user prompts

save_img_bool = ''
while not (save_img_bool == 'y' or save_img_bool == 'n'):
    save_img_bool = input('Do you want to save processed image? (y/n) ')
    
if save_img_bool == 'y':
    if img.shape == processed_img.shape:
        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)
        
    save_img_name = input('Saved image name (name.file_type): ')
    cv2.imwrite('/Users/cobeliu/ImageProcessing/images/' + save_img_name, processed_img)

