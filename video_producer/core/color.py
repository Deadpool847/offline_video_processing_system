"""Color space management and preservation."""

import numpy as np
import cv2
from typing import Dict, Optional


class ColorSpaceManager:
    """Manage color space conversions and preservation."""
    
    COLOR_MATRICES = {
        'bt601': cv2.COLOR_RGB2YUV,
        'bt709': cv2.COLOR_RGB2YUV,
        'bt2020': cv2.COLOR_RGB2YUV,
    }
    
    @staticmethod
    def rgb_to_linear(img: np.ndarray, gamma: float = 2.2) -> np.ndarray:
        """Convert sRGB to linear RGB."""
        img_float = img.astype(np.float32) / 255.0
        linear = np.power(img_float, gamma)
        return linear
    
    @staticmethod
    def linear_to_rgb(img: np.ndarray, gamma: float = 2.2) -> np.ndarray:
        """Convert linear RGB to sRGB."""
        srgb = np.power(np.clip(img, 0, 1), 1.0 / gamma)
        return (srgb * 255).astype(np.uint8)
    
    @staticmethod
    def apply_lut_3d(img: np.ndarray, lut: np.ndarray) -> np.ndarray:
        """Apply 3D LUT to image."""
        # Normalize to LUT space
        img_norm = img.astype(np.float32) / 255.0
        lut_size = lut.shape[0]
        
        # Scale to LUT indices
        coords = img_norm * (lut_size - 1)
        
        # Trilinear interpolation
        r_idx = np.clip(coords[:, :, 0], 0, lut_size - 1)
        g_idx = np.clip(coords[:, :, 1], 0, lut_size - 1)
        b_idx = np.clip(coords[:, :, 2], 0, lut_size - 1)
        
        # Floor and ceiling indices
        r0 = np.floor(r_idx).astype(np.int32)
        g0 = np.floor(g_idx).astype(np.int32)
        b0 = np.floor(b_idx).astype(np.int32)
        
        r1 = np.minimum(r0 + 1, lut_size - 1)
        g1 = np.minimum(g0 + 1, lut_size - 1)
        b1 = np.minimum(b0 + 1, lut_size - 1)
        
        # Fractional parts
        r_frac = r_idx - r0
        g_frac = g_idx - g0
        b_frac = b_idx - b0
        
        # 8 corner lookups
        c000 = lut[r0, g0, b0]
        c001 = lut[r0, g0, b1]
        c010 = lut[r0, g1, b0]
        c011 = lut[r0, g1, b1]
        c100 = lut[r1, g0, b0]
        c101 = lut[r1, g0, b1]
        c110 = lut[r1, g1, b0]
        c111 = lut[r1, g1, b1]
        
        # Interpolate
        r_frac = r_frac[:, :, np.newaxis]
        g_frac = g_frac[:, :, np.newaxis]
        b_frac = b_frac[:, :, np.newaxis]
        
        c00 = c000 * (1 - r_frac) + c100 * r_frac
        c01 = c001 * (1 - r_frac) + c101 * r_frac
        c10 = c010 * (1 - r_frac) + c110 * r_frac
        c11 = c011 * (1 - r_frac) + c111 * r_frac
        
        c0 = c00 * (1 - g_frac) + c10 * g_frac
        c1 = c01 * (1 - g_frac) + c11 * g_frac
        
        result = c0 * (1 - b_frac) + c1 * b_frac
        
        return (result * 255).astype(np.uint8)
    
    @staticmethod
    def load_cube_lut(lut_path: str) -> np.ndarray:
        """Load .cube LUT file."""
        import re
        
        with open(lut_path, 'r') as f:
            lines = f.readlines()
        
        # Parse LUT size
        lut_size = 32  # default
        for line in lines:
            if line.startswith('LUT_3D_SIZE'):
                lut_size = int(line.split()[1])
                break
        
        # Parse LUT data
        lut_data = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('LUT'):
                parts = line.split()
                if len(parts) == 3:
                    try:
                        r, g, b = map(float, parts)
                        lut_data.append([r, g, b])
                    except ValueError:
                        continue
        
        # Reshape to 3D LUT
        lut_array = np.array(lut_data, dtype=np.float32)
        lut_3d = lut_array.reshape(lut_size, lut_size, lut_size, 3)
        
        return lut_3d