import cv2
import numpy as np
from .common import detect_noise, detect_edges, read_image

def unsharp_mask(image, params):
    is_color = len(image.shape) == 3
    
    sigma = params.get('sigma', 1.0)
    amount = params.get('amount', 1.5)
    threshold = params.get('threshold', 0)
    
    if is_color:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        l_sharp = apply_unsharp_mask(l, sigma, amount, threshold)
        
        lab_sharp = cv2.merge([l_sharp, a, b])
        return cv2.cvtColor(lab_sharp, cv2.COLOR_LAB2BGR)
    else:
        return apply_unsharp_mask(image, sigma, amount, threshold)

def apply_unsharp_mask(channel, sigma, amount, threshold):
    gaussian = cv2.GaussianBlur(channel, (0, 0), sigma)
    
    mask = cv2.subtract(channel, gaussian)
    
    if threshold > 0:
        _, mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_TOZERO)
    
    return cv2.addWeighted(channel, 1.0, mask, amount, 0)

def detect_unsharp_mask_params(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
    
    edge_magnitude = detect_edges(gray)
    noise_level = detect_noise(gray)
    
    params = {}
    
    params['sigma'] = 0.5 + edge_magnitude * 2 if edge_magnitude > 0.04 else 1.0
    
    if noise_level > 0.03:
        params['amount'] = max(0.8, 1.5 - noise_level * 10)
    else:
        params['amount'] = min(2.0, 1.5 + edge_magnitude * 2)
    
    params['threshold'] = int(noise_level * 20)
    
    return params

def process_image_with_unsharp_mask(input_path, output_path, params=None):
    try:
        image = read_image(input_path)
        if image is None:
            return False, "Format gambar tidak didukung"
        
        if not params or len(params) == 0:
            params = detect_unsharp_mask_params(image)
        
        result = unsharp_mask(image, params)
        
        cv2.imwrite(output_path, result)
        
        return True, "Gambar berhasil diproses dengan Unsharp Mask"
    
    except Exception as e:
        return False, f"Error: {str(e)}" 