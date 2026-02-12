import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Increase contrast to make text darker and background lighter
    # This helps 'burn out' the faint watermark
    alpha = 1.5 # Contrast control
    beta = 10   # Brightness control
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    
    # Use Otsu's binarization to force pixels to be either pure black or pure white
    _, thresh = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh