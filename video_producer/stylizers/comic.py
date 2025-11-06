"""Comic book / halftone stylizer."""

import numpy as np
import cv2
from typing import Dict, Optional


class ComicStylizer:
    """Comic book effect with halftone patterns."""
    
    def __init__(self,
                 dot_size: int = 3,
                 angle_cyan: float = 15.0,
                 angle_magenta: float = 75.0,
                 angle_yellow: float = 0.0,
                 angle_black: float = 45.0,
                 edge_thickness: int = 2):
        
        self.dot_size = dot_size
        self.angles = {
            'C': angle_cyan,
            'M': angle_magenta,
            'Y': angle_yellow,
            'K': angle_black
        }
        self.edge_thickness = edge_thickness
    
    def process(self, frame: np.ndarray, params: Optional[Dict] = None) -> np.ndarray:
        """Apply comic book effect."""
        # Override params
        if params:
            dot_size = params.get('dot_size', self.dot_size)
        else:
            dot_size = self.dot_size
        
        # Create halftone effect
        halftone = self._create_halftone(frame, dot_size)
        
        # Add bold edges
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Thicken edges
        kernel = np.ones((self.edge_thickness, self.edge_thickness), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Combine
        result = halftone.copy()
        result[edges > 0] = [0, 0, 0]  # Black edges
        
        return result
    
    def _create_halftone(self, img: np.ndarray, dot_size: int) -> np.ndarray:
        """Create CMYK halftone effect."""
        h, w = img.shape[:2]
        
        # Convert to CMYK (approximation)
        rgb_float = img.astype(np.float32) / 255.0
        
        # Simple RGB to CMY conversion
        c = 1.0 - rgb_float[:, :, 0]
        m = 1.0 - rgb_float[:, :, 1]
        y = 1.0 - rgb_float[:, :, 2]
        k = np.minimum(np.minimum(c, m), y)
        
        # Adjust CMY
        c = (c - k) / (1 - k + 1e-6)
        m = (m - k) / (1 - k + 1e-6)
        y = (y - k) / (1 - k + 1e-6)
        
        # Create halftone for each channel
        c_halftone = self._halftone_channel(c, dot_size, self.angles['C'])
        m_halftone = self._halftone_channel(m, dot_size, self.angles['M'])
        y_halftone = self._halftone_channel(y, dot_size, self.angles['Y'])
        k_halftone = self._halftone_channel(k, dot_size, self.angles['K'])
        
        # Combine back to RGB
        c_rgb = np.dstack([c_halftone, np.ones_like(c_halftone), np.ones_like(c_halftone)])
        m_rgb = np.dstack([np.ones_like(m_halftone), m_halftone, np.ones_like(m_halftone)])
        y_rgb = np.dstack([np.ones_like(y_halftone), np.ones_like(y_halftone), y_halftone])
        k_rgb = np.dstack([k_halftone, k_halftone, k_halftone])
        
        # Multiply blend
        result = c_rgb * m_rgb * y_rgb * k_rgb
        result = (result * 255).astype(np.uint8)
        
        return result
    
    def _halftone_channel(self, channel: np.ndarray, dot_size: int, angle: float) -> np.ndarray:
        """Create halftone pattern for a single channel."""
        h, w = channel.shape
        
        # Create dot pattern
        result = np.ones_like(channel)
        
        for y in range(0, h, dot_size * 2):
            for x in range(0, w, dot_size * 2):
                # Get average intensity in region
                y1, y2 = y, min(y + dot_size * 2, h)
                x1, x2 = x, min(x + dot_size * 2, w)
                
                region = channel[y1:y2, x1:x2]
                avg_intensity = np.mean(region)
                
                # Create dot based on intensity
                dot_radius = int((1 - avg_intensity) * dot_size)
                if dot_radius > 0:
                    center_y = (y1 + y2) // 2
                    center_x = (x1 + x2) // 2
                    cv2.circle(result, (center_x, center_y), dot_radius, float(1 - avg_intensity), -1)
        
        return result
    
    def __call__(self, frame: np.ndarray, metadata: Dict) -> np.ndarray:
        """Callable interface for pipeline."""
        return self.process(frame)