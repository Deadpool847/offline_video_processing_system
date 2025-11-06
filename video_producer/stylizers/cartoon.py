"""Cartoon stylizer with edge preservation."""

import numpy as np
import cv2
from typing import Dict, Optional


class CartoonStylizer:
    """Cartoon effect with bilateral filtering and edge detection."""
    
    def __init__(self,
                 bilateral_d: int = 9,
                 bilateral_sigma_color: float = 75.0,
                 bilateral_sigma_space: float = 75.0,
                 edge_threshold1: int = 50,
                 edge_threshold2: int = 150,
                 num_colors: int = 8):
        
        self.bilateral_d = bilateral_d
        self.bilateral_sigma_color = bilateral_sigma_color
        self.bilateral_sigma_space = bilateral_sigma_space
        self.edge_threshold1 = edge_threshold1
        self.edge_threshold2 = edge_threshold2
        self.num_colors = num_colors
    
    def process(self, frame: np.ndarray, params: Optional[Dict] = None) -> np.ndarray:
        """Apply cartoon effect."""
        # Override params if provided
        if params:
            num_colors = params.get('num_colors', self.num_colors)
            bilateral_d = params.get('bilateral_d', self.bilateral_d)
        else:
            num_colors = self.num_colors
            bilateral_d = self.bilateral_d
        
        # Bilateral filter for smoothing while preserving edges
        smoothed = cv2.bilateralFilter(
            frame, 
            bilateral_d,
            self.bilateral_sigma_color,
            self.bilateral_sigma_space
        )
        
        # Color quantization
        quantized = self._quantize_colors(smoothed, num_colors)
        
        # Edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, self.edge_threshold1, self.edge_threshold2)
        
        # Dilate edges
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Convert edges to 3-channel
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        # Combine: darken edges
        result = quantized.copy()
        result[edges > 0] = 0  # Black edges
        
        return result
    
    def _quantize_colors(self, img: np.ndarray, num_colors: int) -> np.ndarray:
        """Quantize colors using k-means."""
        h, w = img.shape[:2]
        
        # Reshape for k-means
        pixels = img.reshape(-1, 3).astype(np.float32)
        
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(
            pixels,
            num_colors,
            None,
            criteria,
            10,
            cv2.KMEANS_RANDOM_CENTERS
        )
        
        # Map pixels to centers
        quantized = centers[labels.flatten()]
        quantized = quantized.reshape(h, w, 3).astype(np.uint8)
        
        return quantized
    
    def __call__(self, frame: np.ndarray, metadata: Dict) -> np.ndarray:
        """Callable interface for pipeline."""
        return self.process(frame)