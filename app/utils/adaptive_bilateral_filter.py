import cv2
import numpy as np
from .common import detect_noise, detect_edges, read_image

DEFAULT_DOMAIN_SIGMA = 0.1
DEFAULT_RANGE_SIGMA = 20
DEFAULT_KERNEL_SIZE = (5, 5)
DEFAULT_CLAHE_CLIP_LIMIT = 2.0
DEFAULT_CLAHE_GRID_SIZE = (8, 8)

def analyze_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
    
    noise_level = detect_noise(gray)
    edge_magnitude = detect_edges(gray)
    
    params = {}
    height, width = image.shape[:2]
    
    if noise_level > 0.05:
        params['domain_sigma'] = 0.2 + noise_level * 2
        params['range_sigma'] = max(10, 30 - noise_level * 100)
        params['denoise_strength'] = min(20, noise_level * 200)
        params['enhancement_amount'] = 0
    elif edge_magnitude > 0.02:
        params['domain_sigma'] = 0.1 + edge_magnitude
        params['range_sigma'] = 20 - edge_magnitude * 50
        params['denoise_strength'] = min(10, noise_level * 100)
        params['enhancement_amount'] = 0.5
    else:
        params['domain_sigma'] = DEFAULT_DOMAIN_SIGMA
        params['range_sigma'] = DEFAULT_RANGE_SIGMA
        params['denoise_strength'] = min(5, noise_level * 60)
        params['enhancement_amount'] = 0.3
    
    params['window_size'] = max(3, min(9, int(min(height, width) / 150) * 2 + 1))
    if params['window_size'] % 2 == 0:
        params['window_size'] += 1
    
    mean_brightness = np.mean(gray) / 255.0
    if mean_brightness < 0.3:
        params['offset'] = int(10 * (0.5 - mean_brightness))
    elif mean_brightness > 0.7:
        params['offset'] = int(-10 * (mean_brightness - 0.5))
    else:
        params['offset'] = 0
    
    return params

def detect_edges_for_abf(image):
    log_kernel_size = 5
    log_sigma = 0.5
    log_image = cv2.GaussianBlur(image, (log_kernel_size, log_kernel_size), log_sigma)
    log_image = cv2.Laplacian(log_image, cv2.CV_32F, ksize=3)
    
    log_image = np.abs(log_image)
    log_image = cv2.normalize(log_image, None, 0, 1, cv2.NORM_MINMAX)
    
    return log_image

def apply_adaptive_bilateral_filter(image, edge_map, window_size, domain_sigma, range_sigma_base):
    height, width = image.shape
    result = np.zeros_like(image, dtype=np.float32)
    padding = window_size // 2
    
    padded = cv2.copyMakeBorder(image, padding, padding, padding, padding, cv2.BORDER_REFLECT)
    
    spatial_kernel = np.zeros((window_size, window_size), dtype=np.float32)
    for i in range(window_size):
        for j in range(window_size):
            x = j - padding
            y = i - padding
            dist_sq = x*x + y*y
            spatial_kernel[i, j] = np.exp(-dist_sq / (2 * domain_sigma * domain_sigma))
    
    for i in range(height):
        for j in range(width):
            edge_strength = edge_map[i, j]
            
            window = padded[i:i+window_size, j:j+window_size].astype(np.float32)
            center_val = float(image[i, j])
            
            offset = 10.0 * edge_strength
            range_sigma = range_sigma_base * (1.0 - 0.5 * edge_strength)
            
            diff = window - (center_val + offset)
            range_weights = np.exp(-(diff * diff) / (2. * range_sigma * range_sigma))
            weights = spatial_kernel * range_weights
            
            weights_sum = np.sum(weights)
            if weights_sum > 0:
                normalized_weights = weights / weights_sum
            else:
                normalized_weights = np.ones_like(weights) / np.size(weights)
            
            result[i, j] = np.sum(window * normalized_weights)
    
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)

def adaptive_bilateral_filter(image, params):
    is_color = len(image.shape) == 3
    
    domain_sigma = params.get('domain_sigma', DEFAULT_DOMAIN_SIGMA)
    range_sigma = params.get('range_sigma', DEFAULT_RANGE_SIGMA)
    window_size = params.get('window_size', 5)
    
    if is_color:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        edge_image = detect_edges_for_abf(l)
        l_filtered = apply_adaptive_bilateral_filter(l, edge_image, window_size, domain_sigma, range_sigma)
        
        enhanced = cv2.merge([l_filtered, a, b])
        result = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    else:
        edge_image = detect_edges_for_abf(image)
        result = apply_adaptive_bilateral_filter(image, edge_image, window_size, domain_sigma, range_sigma)
    
    result = enhance_contrast(result, is_color)
    
    return result

def enhance_contrast(image, is_color):
    if is_color:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=DEFAULT_CLAHE_CLIP_LIMIT, tileGridSize=DEFAULT_CLAHE_GRID_SIZE)
        enhanced_l = clahe.apply(l)
        
        enhanced = cv2.merge([enhanced_l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=DEFAULT_CLAHE_CLIP_LIMIT, tileGridSize=DEFAULT_CLAHE_GRID_SIZE)
        return clahe.apply(image)

def denoise_image(image, strength):
    if len(image.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(image, None, strength, strength, 7, 21)
    else:
        return cv2.fastNlMeansDenoising(image, None, strength, 7, 21)

def process_image(input_path, output_path, params=None):
    try:
        image = read_image(input_path)
        if image is None:
            return False, "Format gambar tidak didukung"
        
        if not params or len(params) == 0:
            params = analyze_image(image)
        
        denoise_strength = params.get('denoise_strength', 0)
        if denoise_strength > 0:
            image = denoise_image(image, denoise_strength)
        
        result = adaptive_bilateral_filter(image, params)
        
        enhancement_amount = params.get('enhancement_amount', 0.3)
        if enhancement_amount > 0:
            enhanced = cv2.addWeighted(image, 1 + enhancement_amount, result, -enhancement_amount, 0)
            result = cv2.addWeighted(result, 1 - enhancement_amount, enhanced, enhancement_amount, 0)
        
        cv2.imwrite(output_path, result)
        
        return True, "Gambar berhasil diproses dengan Adaptive Bilateral Filter"
    
    except Exception as e:
        return False, f"Error: {str(e)}"