"""Fast neural style transfer using ONNX."""

import numpy as np
import cv2
from typing import Dict, Optional
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.ml_session import MLSession


class FastStyleStylizer:
    """Fast neural style transfer with ONNX."""
    
    def __init__(self,
                 model_path: str,
                 tile_size: int = 512,
                 overlap: int = 32,
                 use_gpu: bool = True):
        
        self.model_path = model_path
        self.tile_size = tile_size
        self.overlap = overlap
        self.use_gpu = use_gpu
        self.session = None
        
        if Path(model_path).exists():
            try:
                self.session = MLSession(model_path, use_gpu=use_gpu)
            except Exception as e:
                print(f"Failed to load ONNX model: {e}")
                self.session = None
    
    def process(self, frame: np.ndarray, params: Optional[Dict] = None) -> np.ndarray:
        """Apply neural style transfer."""
        if self.session is None:
            # Fallback: return original frame with slight blur
            return cv2.GaussianBlur(frame, (5, 5), 0)
        
        try:
            # Use tiled inference for large images
            if frame.shape[0] > self.tile_size or frame.shape[1] > self.tile_size:
                result = self.session.infer_tiled(
                    frame,
                    tile_size=self.tile_size,
                    overlap=self.overlap
                )
            else:
                # Direct inference
                result = self.session._infer_single(frame)
            
            return result
            
        except Exception as e:
            print(f"Style transfer failed: {e}")
            return frame
    
    def __call__(self, frame: np.ndarray, metadata: Dict) -> np.ndarray:
        """Callable interface for pipeline."""
        return self.process(frame)