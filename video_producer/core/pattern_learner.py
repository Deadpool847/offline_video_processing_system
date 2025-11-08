"""Pattern learning system for intelligent parameter optimization."""

import numpy as np
import cv2
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class PatternLearner:
    """Learns from video patterns to optimize processing parameters."""
    
    def __init__(self):
        self.learned_patterns = {}
    
    def analyze_video(self, sample_frames: List[np.ndarray]) -> Dict:
        """Analyze video characteristics from sample frames."""
        if not sample_frames:
            return self._get_default_characteristics()
        
        characteristics = {
            'brightness': 0.0,
            'contrast': 0.0,
            'edge_density': 0.0,
            'color_richness': 0.0,
            'noise_level': 0.0,
            'motion_estimate': 0.0
        }
        
        # Analyze each frame
        for frame in sample_frames:
            # Brightness (mean luminance)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            characteristics['brightness'] += np.mean(gray) / 255.0
            
            # Contrast (std of luminance)
            characteristics['contrast'] += np.std(gray) / 128.0
            
            # Edge density
            edges = cv2.Canny(gray, 50, 150)
            characteristics['edge_density'] += np.sum(edges > 0) / edges.size
            
            # Color richness (color variance)
            color_std = np.mean([np.std(frame[:,:,c]) for c in range(3)])
            characteristics['color_richness'] += color_std / 128.0
            
            # Noise level (high-frequency content)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            characteristics['noise_level'] += np.var(laplacian) / 10000.0
        
        # Average across frames
        n_frames = len(sample_frames)
        for key in characteristics:
            characteristics[key] /= n_frames
            characteristics[key] = np.clip(characteristics[key], 0.0, 1.0)
        
        return characteristics
    
    def get_optimized_params(self, characteristics: Dict, styles: List[str]) -> Dict:
        """Get optimized parameters based on video characteristics."""
        params = {}
        
        for style in styles:
            if 'Pencil' in style:
                params[style] = self._optimize_pencil(characteristics)
            elif 'Cartoon' in style:
                params[style] = self._optimize_cartoon(characteristics)
            elif 'Comic' in style:
                params[style] = self._optimize_comic(characteristics)
            elif 'Cinematic' in style:
                params[style] = self._optimize_cinematic(characteristics)
        
        return params
    
    def _optimize_pencil(self, char: Dict) -> Dict:
        """Optimize pencil sketch parameters."""
        # High contrast content needs less blur
        # Low edge content needs more edge enhancement
        
        base_blur = 21.0
        
        if char['contrast'] > 0.7:
            blur_sigma = base_blur * 0.7  # Less blur for high contrast
        elif char['contrast'] < 0.3:
            blur_sigma = base_blur * 1.3  # More blur for low contrast
        else:
            blur_sigma = base_blur
        
        return {
            'blur_sigma': blur_sigma,
            'use_texture': char['noise_level'] < 0.3  # Add texture if clean
        }
    
    def _optimize_cartoon(self, char: Dict) -> Dict:
        """Optimize cartoon parameters."""
        # More colors for color-rich content
        # Stronger edges for low-edge content
        
        if char['color_richness'] > 0.7:
            num_colors = 12
        elif char['color_richness'] > 0.4:
            num_colors = 8
        else:
            num_colors = 6
        
        if char['edge_density'] < 0.2:
            edge_threshold1 = 30  # More sensitive
            edge_threshold2 = 120
        else:
            edge_threshold1 = 50  # Standard
            edge_threshold2 = 150
        
        return {
            'num_colors': num_colors,
            'edge_threshold1': edge_threshold1,
            'edge_threshold2': edge_threshold2
        }
    
    def _optimize_comic(self, char: Dict) -> Dict:
        """Optimize comic/halftone parameters."""
        # Adjust dot size based on resolution and detail
        
        if char['edge_density'] > 0.5:
            dot_size = 2  # Smaller dots for detailed content
        elif char['edge_density'] > 0.3:
            dot_size = 3
        else:
            dot_size = 4  # Larger dots for simple content
        
        return {
            'dot_size': dot_size,
            'edge_thickness': 2
        }
    
    def _optimize_cinematic(self, char: Dict) -> Dict:
        """Optimize cinematic grading parameters."""
        # Adjust bloom for brightness
        # Adjust grain for noise level
        
        if char['brightness'] > 0.7:
            bloom = 0.4  # More bloom for bright scenes
        elif char['brightness'] < 0.3:
            bloom = 0.2  # Less bloom for dark scenes
        else:
            bloom = 0.3
        
        if char['noise_level'] < 0.2:
            grain = 0.03  # Add grain to clean footage
        else:
            grain = 0.01  # Less grain if already noisy
        
        return {
            'bloom_strength': bloom,
            'grain_strength': grain,
            'vignette_strength': 0.4
        }
    
    def _get_default_characteristics(self) -> Dict:
        """Get default characteristics when analysis fails."""
        return {
            'brightness': 0.5,
            'contrast': 0.5,
            'edge_density': 0.3,
            'color_richness': 0.5,
            'noise_level': 0.2,
            'motion_estimate': 0.5
        }