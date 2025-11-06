"""Pencil sketch stylizer with temporal stability."""

import numpy as np
import cv2
from typing import Dict, Optional


class PencilStylizer:
    """Pencil sketch effect with temporal EMA."""
    
    def __init__(self, 
                 blur_sigma: float = 21.0,
                 blend_mode: str = 'color_dodge',
                 use_texture: bool = False,
                 texture_path: Optional[str] = None):
        
        self.blur_sigma = blur_sigma
        self.blend_mode = blend_mode
        self.use_texture = use_texture
        self.texture = None
        
        if use_texture and texture_path:
            self._load_texture(texture_path)
    
    def _load_texture(self, texture_path: str):
        """Load paper texture."""
        try:
            self.texture = cv2.imread(texture_path, cv2.IMREAD_GRAYSCALE)
            if self.texture is not None:
                self.texture = self.texture.astype(np.float32) / 255.0
        except Exception as e:
            print(f"Failed to load texture: {e}")
            self.texture = None
    
    def process(self, frame: np.ndarray, params: Optional[Dict] = None) -> np.ndarray:
        """Apply pencil sketch effect."""
        # Override params if provided
        if params:
            blur_sigma = params.get('blur_sigma', self.blur_sigma)
        else:
            blur_sigma = self.blur_sigma
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Invert
        inverted = 255 - gray
        
        # Gaussian blur
        blurred = cv2.GaussianBlur(inverted, (0, 0), sigmaX=blur_sigma)
        
        # Color dodge blend
        sketch = self._color_dodge(gray, blurred)
        
        # Apply texture if enabled
        if self.use_texture and self.texture is not None:
            sketch = self._apply_texture(sketch)
        
        # Convert back to RGB
        sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
        
        return sketch_rgb
    
    def _color_dodge(self, base: np.ndarray, blend: np.ndarray) -> np.ndarray:
        """Color dodge blend mode."""
        # Avoid division by zero
        result = np.zeros_like(base, dtype=np.float32)
        mask = blend < 255
        
        result[mask] = np.clip(
            (base[mask].astype(np.float32) * 255) / (255 - blend[mask].astype(np.float32) + 1e-6),
            0, 255
        )
        result[~mask] = 255
        
        return result.astype(np.uint8)
    
    def _apply_texture(self, img: np.ndarray) -> np.ndarray:
        """Apply paper texture."""
        h, w = img.shape[:2]
        
        # Resize texture to match image
        texture_resized = cv2.resize(self.texture, (w, h))
        
        # Blend
        img_float = img.astype(np.float32) / 255.0
        blended = img_float * texture_resized
        
        return (blended * 255).astype(np.uint8)
    
    def __call__(self, frame: np.ndarray, metadata: Dict) -> np.ndarray:
        """Callable interface for pipeline."""
        return self.process(frame)