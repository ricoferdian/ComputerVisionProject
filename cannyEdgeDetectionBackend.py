from scipy import ndimage
from scipy.ndimage.filters import convolve

import numpy as np
import matplotlib.pyplot as plt

from skimage import feature

from scipy import misc
import numpy as np
import operasiTitikBackend as operasiTitik
import cv2

def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size + 1, -size:size + 1]
    normal = 1 / (2.0 * np.pi * sigma ** 2)
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
    return g

def sobel_filters(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)

    Ix = convolve(img, Kx)
    Iy = convolve(img, Ky)

    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)
    return (G, theta)


def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M, N), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            try:
                q = 255
                r = 255

                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j + 1]
                    r = img[i, j - 1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i + 1, j - 1]
                    r = img[i - 1, j + 1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i + 1, j]
                    r = img[i - 1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i - 1, j - 1]
                    r = img[i + 1, j + 1]

                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0


            except IndexError as e:
                pass

    return Z

def threshold(img, lowThreshold, highThreshold, weak_pixel, strong_pixel):
    highThreshold = img.max() * highThreshold
    lowThreshold = highThreshold * lowThreshold

    M, N = img.shape
    res = np.zeros((M, N), dtype=np.int32)

    weak = np.int32(weak_pixel)
    strong = np.int32(strong_pixel)

    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)

    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return (res)


def hysteresis(img, weak_pixel, strong_pixel):
    M, N = img.shape
    weak = weak_pixel
    strong = strong_pixel

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            if (img[i, j] == weak):
                try:
                    if ((img[i + 1, j - 1] == strong) or (img[i + 1, j] == strong) or (img[i + 1, j + 1] == strong)
                            or (img[i, j - 1] == strong) or (img[i, j + 1] == strong)
                            or (img[i - 1, j - 1] == strong) or (img[i - 1, j] == strong) or (
                                    img[i - 1, j + 1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img

def rgbGaussianBlur(imgs,height, width, color, kernel_size, sigma):
    imgs_final = []
    if color is 3:
        for channel in range(color):
            if(channel is 0):
                image = operasiTitik.getR2D(imgs, height, width, color)
            elif(channel is 1):
                image = operasiTitik.getG2D(imgs, height, width, color)
            else:
                image = operasiTitik.getB2D(imgs, height, width, color)
            img_smoothed = gaussianBlur(image,height, width, 1, kernel_size, sigma)
            # gradientMat, thetaMat = sobel_filters(img_smoothed)
            # nonMaxImg = non_max_suppression(gradientMat, thetaMat)
            # thresholdImg = threshold(nonMaxImg)
            # img_final = hysteresis(thresholdImg)
            imgs_final.append(img_smoothed)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[1],imgs_final[2],height, width)
    else:
        image = operasiTitik.getR2D(imgs, height, width, color)
        img_smoothed = gaussianBlur(image,height, width, 1, kernel_size, sigma)
        imgs_final.append(img_smoothed)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[0],imgs_final[0],height, width)
    return np.array(result)

def sobelFilterRgb(imgs,height, width, color):
    imgs_final = []
    if color is 3:
        for channel in range(color):
            if(channel is 0):
                image = operasiTitik.getR2D(imgs, height, width, color)
            elif(channel is 1):
                image = operasiTitik.getG2D(imgs, height, width, color)
            else:
                image = operasiTitik.getB2D(imgs, height, width, color)
            gradientMat, thetaMat = sobel_filters(image)
            # gradientMat, thetaMat = sobel_filters(img_smoothed)
            # nonMaxImg = non_max_suppression(gradientMat, thetaMat)
            # thresholdImg = threshold(nonMaxImg)
            # img_final = hysteresis(thresholdImg)
            imgs_final.append(gradientMat)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[1],imgs_final[2],height, width)
    else:
        image = operasiTitik.getR2D(imgs, height, width, color)
        gradientMat, thetaMat = sobel_filters(image)
        imgs_final.append(gradientMat)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[0],imgs_final[0],height, width)
    return np.array(result)

def gaussianBlur(image,height, width, color, kernel_size, sigma):
    kernel = gaussian_kernel(kernel_size, sigma)
    print('using kernel',kernel)
    return convolve(image, kernel)

def edgeDetection(imgs, height, width, color, sigma=1, kernel_size=5, weak_pixel=75, strong_pixel=255, lowthreshold=0.05,
             highthreshold=0.15):
    imgs_final = []
    if color is 3:
        for channel in range(color):
            if(channel is 0):
                image = operasiTitik.getR2D(imgs, height, width, color)
            elif(channel is 1):
                image = operasiTitik.getG2D(imgs, height, width, color)
            else:
                image = operasiTitik.getB2D(imgs, height, width, color)
            img_smoothed = gaussianBlur(image,height, width, 1, kernel_size, sigma)
            # gradientMat, thetaMat = sobel_filters(img_smoothed)
            # nonMaxImg = non_max_suppression(gradientMat, thetaMat)
            # thresholdImg = threshold(nonMaxImg)
            # img_final = hysteresis(thresholdImg)
            imgs_final.append(img_smoothed)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[1],imgs_final[2],height, width)
    else:
        image = operasiTitik.getR2D(imgs, height, width, color)
        img_smoothed = gaussianBlur(image,height, width, 1, kernel_size, sigma)
        print("self.img_smoothed",img_smoothed)
        gradientMat, thetaMat = sobel_filters(img_smoothed)
        nonMaxImg = non_max_suppression(gradientMat, thetaMat)
        thresholdImg = threshold(nonMaxImg, lowthreshold, highthreshold, weak_pixel, strong_pixel)
        img_final = hysteresis(thresholdImg, weak_pixel, strong_pixel)
        imgs_final.append(img_final)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[0],imgs_final[0],height, width)
    print(result.shape)
    return np.array(result)

def opencv_canny(image,threshold1,threshold2):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Find the edges in the image using canny detector
    edges = cv2.Canny(gray, threshold1, threshold2)
    rgbimg = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return rgbimg

def scikit_canny(imgs,height,width,color,sigma):
    print('sigma scikit_canny',sigma)
    imgs_final = []
    if color is 3:
        for channel in range(color):
            if(channel is 0):
                image = operasiTitik.getR2D(imgs, height, width, color)
            elif(channel is 1):
                image = operasiTitik.getG2D(imgs, height, width, color)
            else:
                image = operasiTitik.getB2D(imgs, height, width, color)
            img_canny = feature.canny(image, sigma=sigma)
            imgs_final.append(img_canny)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[1],imgs_final[2],height, width)
    else:
        image = operasiTitik.bin2Bin2dBinary(imgs, height, width, color)
        image = np.array(image,dtype='float32')
        image = np.zeros((128, 128))
        image[32:-32, 32:-32] = 1
        print('image',image)
        image = ndimage.gaussian_filter(image, 4)
        print('image',image)
        img_canny = feature.canny(image, sigma=10)
        print('img_canny',img_canny)
        imgs_final.append(img_canny)

        imgs_final = np.array(imgs_final).astype(dtype='float32')
        imgs_final = operasiTitik.binary2dtobin(imgs_final,128, 128)
        print('imgs_final',imgs_final)
        result = operasiTitik.combineRGB2DtoRGB(imgs_final[0],imgs_final[0],imgs_final[0],128, 128)
        print('result',result)

    return np.array(result).astype(dtype='float32')
