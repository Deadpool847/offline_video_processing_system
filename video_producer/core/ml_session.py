"""ML inference session with ONNX Runtime."""

import numpy as np
import onnxruntime as ort
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class MLSession:
    """ONNX Runtime session manager."""
    
    def __init__(self, model_path: str, use_gpu: bool = True):
        self.model_path = model_path
        self.use_gpu = use_gpu
        self.session = None
        self._init_session()
    
    def _init_session(self):
        """Initialize ONNX Runtime session."""
        providers = self._get_providers()
        
        try:
            self.session = ort.InferenceSession(
                self.model_path,
                providers=providers
            )
            
            logger.info(f"Loaded model: {self.model_path}")
            logger.info(f"Providers: {self.session.get_providers()}")
            
            # Log input/output info
            input_name = self.session.get_inputs()[0].name
            input_shape = self.session.get_inputs()[0].shape
            logger.info(f"Input: {input_name} {input_shape}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _get_providers(self) -> List[str]:
        """Get available execution providers."""
        available = ort.get_available_providers()
        
        if self.use_gpu and 'CUDAExecutionProvider' in available:
            return ['CUDAExecutionProvider', 'CPUExecutionProvider']
        else:
            return ['CPUExecutionProvider']
    
    def infer(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference."""
        if self.session is None:
            raise RuntimeError("Session not initialized")
        
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name
        
        result = self.session.run(
            [output_name],
            {input_name: input_data}
        )
        
        return result[0]
    
    def infer_tiled(self, 
                    img: np.ndarray,
                    tile_size: int = 512,
                    overlap: int = 32) -> np.ndarray:
        """Infer with tiling for large images."""
        h, w = img.shape[:2]
        
        # If image fits in tile, process directly
        if h <= tile_size and w <= tile_size:
            return self._infer_single(img)
        
        # Process with overlapping tiles
        output = np.zeros_like(img)
        weight_map = np.zeros((h, w), dtype=np.float32)
        
        stride = tile_size - overlap
        
        for y in range(0, h, stride):
            for x in range(0, w, stride):
                # Extract tile
                y1 = y
                y2 = min(y + tile_size, h)
                x1 = x
                x2 = min(x + tile_size, w)
                
                tile = img[y1:y2, x1:x2]
                
                # Pad if needed
                pad_h = tile_size - tile.shape[0]
                pad_w = tile_size - tile.shape[1]
                if pad_h > 0 or pad_w > 0:
                    tile = np.pad(tile, ((0, pad_h), (0, pad_w), (0, 0)), mode='reflect')
                
                # Process tile
                result_tile = self._infer_single(tile)
                
                # Remove padding
                result_tile = result_tile[:y2-y1, :x2-x1]
                
                # Blend with feathering
                weight = self._create_weight_map(result_tile.shape[0], result_tile.shape[1], overlap)
                
                output[y1:y2, x1:x2] += result_tile * weight[:, :, np.newaxis]
                weight_map[y1:y2, x1:x2] += weight
        
        # Normalize by weight
        weight_map = np.maximum(weight_map, 1e-6)
        output = output / weight_map[:, :, np.newaxis]
        
        return output.astype(np.uint8)
    
    def _infer_single(self, img: np.ndarray) -> np.ndarray:
        """Infer single image (internal helper)."""
        # Prepare input (NCHW format)
        input_data = img.astype(np.float32) / 255.0
        input_data = np.transpose(input_data, (2, 0, 1))
        input_data = np.expand_dims(input_data, axis=0)
        
        # Infer
        output = self.infer(input_data)
        
        # Convert back (NHWC)
        output = np.squeeze(output, axis=0)
        output = np.transpose(output, (1, 2, 0))
        output = np.clip(output * 255.0, 0, 255).astype(np.uint8)
        
        return output
    
    def _create_weight_map(self, h: int, w: int, overlap: int) -> np.ndarray:
        """Create feathering weight map."""
        weight = np.ones((h, w), dtype=np.float32)
        
        # Feather edges
        if overlap > 0:
            for i in range(overlap):
                alpha = i / overlap
                weight[i, :] = alpha
                weight[-i-1, :] = alpha
                weight[:, i] = alpha
                weight[:, -i-1] = alpha
        
        return weight