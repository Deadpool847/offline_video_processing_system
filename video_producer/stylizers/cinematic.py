"""Cinematic grading with LUTs and effects."""

import numpy as np
import cv2
from typing import Dict, Optional
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.color import ColorSpaceManager


class CinematicStylizer:
    """Cinematic grading with 3D LUT, bloom, grain, and vignette."""
    
    def __init__(self,
                 lut_path: Optional[str] = None,
                 bloom_strength: float = 0.3,
                 grain_strength: float = 0.02,
                 vignette_strength: float = 0.4):
        
        self.lut = None
        self.bloom_strength = bloom_strength
        self.grain_strength = grain_strength
        self.vignette_strength = vignette_strength
        self.color_manager = ColorSpaceManager()
        
        if lut_path and Path(lut_path).exists():
            self._load_lut(lut_path)
    
    def _load_lut(self, lut_path: str):
        """Load 3D LUT."""
        try:
            self.lut = self.color_manager.load_cube_lut(lut_path)
        except Exception as e:
            print(f"Failed to load LUT: {e}")
            self.lut = None
    
    def process(self, frame: np.ndarray, params: Optional[Dict] = None) -> np.ndarray:
        """Apply cinematic grading."""
        result = frame.copy().astype(np.float32) / 255.0
        
        # Override params
        if params:
            bloom_strength = params.get('bloom_strength', self.bloom_strength)
            grain_strength = params.get('grain_strength', self.grain_strength)
            vignette_strength = params.get('vignette_strength', self.vignette_strength)
        else:
            bloom_strength = self.bloom_strength
            grain_strength = self.grain_strength
            vignette_strength = self.vignette_strength
        
        # Apply LUT if available
        if self.lut is not None:
            result = self._apply_lut(result)
        else:
            # Simple tone curve as fallback
            result = self._apply_tone_curve(result)
        
        # Add bloom
        if bloom_strength > 0:
            result = self._add_bloom(result, bloom_strength)
        
        # Add film grain
        if grain_strength > 0:
            result = self._add_grain(result, grain_strength)
        
        # Add vignette
        if vignette_strength > 0:
            result = self._add_vignette(result, vignette_strength)
        
        # Convert back to uint8
        result = np.clip(result * 255, 0, 255).astype(np.uint8)
        
        return result
    
    def _apply_lut(self, img: np.ndarray) -> np.ndarray:
        """Apply 3D LUT."""
        img_uint8 = (img * 255).astype(np.uint8)
        result = self.color_manager.apply_lut_3d(img_uint8, self.lut)
        return result.astype(np.float32) / 255.0
    
    def _apply_tone_curve(self, img: np.ndarray) -> np.ndarray:
        """Apply simple S-curve for contrast."""
        # S-curve using gamma adjustment
        shadows = np.power(img, 1.2)  # Lift shadows
        highlights = 1 - np.power(1 - img, 1.2)  # Compress highlights
        
        # Blend based on luminance
        luma = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
        mask = luma[:, :, np.newaxis]
        
        result = shadows * (1 - mask) + highlights * mask
        return result
    
    def _add_bloom(self, img: np.ndarray, strength: float) -> np.ndarray:
        """Add bloom/glow effect."""
        # Extract bright areas
        bright = np.maximum(img - 0.7, 0) * (1 / 0.3)
        
        # Blur bright areas
        bright_uint8 = (bright * 255).astype(np.uint8)
        bloom = cv2.GaussianBlur(bright_uint8, (0, 0), sigmaX=15)
        bloom = bloom.astype(np.float32) / 255.0
        
        # Add bloom
        result = img + bloom * strength
        return np.clip(result, 0, 1)
    
    def _add_grain(self, img: np.ndarray, strength: float) -> np.ndarray:
        """Add film grain."""
        h, w = img.shape[:2]
        
        # Generate grain
        grain = np.random.randn(h, w, 3).astype(np.float32) * strength
        
        # Add grain
        result = img + grain
        return np.clip(result, 0, 1)
    
    def _add_vignette(self, img: np.ndarray, strength: float) -> np.ndarray:
        """Add vignette effect."""
        h, w = img.shape[:2]
        
        # Create radial gradient
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h / 2, w / 2
        
        # Distance from center
        max_dist = np.sqrt(center_y**2 + center_x**2)
        dist = np.sqrt((y - center_y)**2 + (x - center_x)**2)
        
        # Vignette mask
        vignette = 1 - (dist / max_dist) * strength
        vignette = np.clip(vignette, 0, 1)
        
        # Apply vignette
        result = img * vignette[:, :, np.newaxis]
        return result
    
    def __call__(self, frame: np.ndarray, metadata: Dict) -> np.ndarray:
        """Callable interface for pipeline."""
        return self.process(frame)