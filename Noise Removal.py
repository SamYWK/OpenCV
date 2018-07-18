# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 13:01:01 2018

@author: pig84
"""

import cv2
import numpy as np
import sys

def options():
    #option selection
    while(True):
        print('==============Noise Removal==============')
        print('Which file are you going to load?')
        print('\n1)lena_grey.jpg\
               \n2)lena_color.jpg\
               \n0)Exit')
        option_num = input('Input number : ')
        if option_num == '1' or option_num == '2':
            break
        elif option_num == '0':
            sys.exit(0)
        else:
            print('\nMust select correct number !\n')
    return option_num
    
def load_src_img(file_name):
    src_img = cv2.imread(file_name)
    m, n, channel = src_img.shape
    return src_img, m, n

def add_noise(img, m, n, img_type):
    noise_count = 10000
    #change type
    if img_type == 'grey':
        img = img.astype(np.int)
        #noise position
        x = np.random.randint(m, size = noise_count)
        y = np.random.randint(n, size = noise_count)
        
        for i in range(noise_count):
            noise_level = np.random.randint(low = -255, high = 256, size = 1)
            img[x[i], y[i]] = img[x[i], y[i]] + noise_level
            
    elif img_type == 'color':
        img = img.astype(np.int)
        #noise position
        x = np.random.randint(m, size = noise_count)
        y = np.random.randint(n, size = noise_count)
        
        for i in range(noise_count):
            noise_level = np.random.randint(low = -255, high = 256, size = 1)
            img[x[i], y[i], :] = img[x[i], y[i], :] + noise_level
    return img

def noise_removal(img, noise_img_count):
    m, n = img.shape
    
    #for every pixel
    for x in range(m):
        for y in range(n):
            img[x, y] = int(img[x, y]/noise_img_count)
    return img.astype(np.uint8)

def show_image(img, name):
    cv2.imshow(name, img)   
    cv2.waitKey (0)  
    cv2.destroyAllWindows()
    return None
    
def main():
    option_num = options()
    #=========================gray level=========================
    if option_num == '1':
        #noise image count
        noise_img_count = 20
        
        #load image
        src_img, m, n = load_src_img('./data/lena_grey.jpg')
        show_image(src_img, 'Source Image_grey')
        src_img = src_img[:, :, 0].reshape(m, n)
        
        #noise image
        noise_img = add_noise(src_img, m, n, 'grey') 
        #show noise image
        show_image(noise_img.astype(np.uint8), 'Noise_Image')
        #save image
        cv2.imwrite('./data/lena_grey_noise.jpg', noise_img.astype(np.uint8))
        
        #generate count - 1 noise_images
        for i in range(noise_img_count - 1):  
            noise_img = noise_img + add_noise(src_img, m, n, 'grey')
        
        #revert image
        revert_img = noise_removal(noise_img, noise_img_count)
        #show revert image
        show_image(revert_img, 'Revert_Image')
        #save image
        cv2.imwrite('./data/lena_grey_revert.jpg', revert_img)
    
    
    #============================color===========================
    elif option_num == '2':
        #noise image count
        noise_img_count = 20
        
        #load image
        src_img, m, n = load_src_img('./data/lena_color.jpg')
        show_image(src_img, 'Source Image_color')
        
        #noise image
        noise_img = add_noise(src_img, m, n, 'color')
        show_image(noise_img.astype(np.uint8), 'Noise_Image')
        #save image
        cv2.imwrite('./data/lena_color_noise.jpg', noise_img.astype(np.uint8))
        
        #convert BGR to HSV. I just want the V value
        HSV_img_V = cv2.cvtColor(noise_img.astype(np.uint8), cv2.COLOR_BGR2HSV)[:, :, 2]
        HSV_img_HS = cv2.cvtColor(noise_img.astype(np.uint8), cv2.COLOR_BGR2HSV)[:, :, 0:2]
        
        #generate count - 1 noise_images
        for i in range(noise_img_count - 1):  
            HSV_img_V = HSV_img_V + cv2.cvtColor(add_noise(src_img, m, n, 'color').astype(np.uint8), cv2.COLOR_BGR2HSV)[:, :, 2].astype(np.int)
        
        #revert image
        revert_img_V = noise_removal(HSV_img_V, noise_img_count).reshape(m, n, 1)
        revert_img = np.concatenate([HSV_img_HS, revert_img_V], axis = 2)
        
        #convert HSV to BGR
        BGR_img = cv2.cvtColor(revert_img, cv2.COLOR_HSV2BGR)
        show_image(BGR_img, 'Revert_Image')
        #save image
        cv2.imwrite('./data/lena_color_revert.jpg', BGR_img)
    
    print('All pictures are saved in ./data.')
if __name__ == "__main__":
    main()