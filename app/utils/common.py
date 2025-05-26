import cv2
import numpy as np
import os
from PIL import Image

def detect_noise(gray_image):
    median_filtered = cv2.medianBlur(gray_image, 3)
    noise_diff = cv2.absdiff(gray_image, median_filtered)
    return np.mean(noise_diff) / 255.0

def detect_edges(gray_image):
    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    edge_magnitude = cv2.magnitude(sobel_x, sobel_y)
    edge_magnitude = cv2.normalize(edge_magnitude, None, 0, 1, cv2.NORM_MINMAX)
    return np.mean(edge_magnitude)

def read_image(input_path):
    image = cv2.imread(input_path)
    
    if image is None:
        try:
            pil_image = Image.open(input_path)
            pil_image = pil_image.convert('RGB')
            
            temp_path = input_path + '.temp.jpg'
            pil_image.save(temp_path)
            image = cv2.imread(temp_path)
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            return None
    
    return image