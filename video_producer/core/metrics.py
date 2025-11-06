"""Metrics collection for ML feedback."""

import numpy as np
import cv2
from typing import Dict, List
import time
from pathlib import Path
import json


class MetricsCollector:
    """Collect processing metrics for ML learning."""
    
    def __init__(self, output_dir: str = "logs/metrics"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_log = []
    
    def collect_frame_metrics(self, 
                             original: np.ndarray,
                             processed: np.ndarray,
                             style: str,
                             frame_idx: int,
                             processing_time: float) -> Dict:
        """Collect metrics for a single frame."""
        metrics = {
            'frame_idx': frame_idx,
            'style': style,
            'processing_time': processing_time,
            'edge_coherence': self._edge_coherence(processed),
            'ssim': self._ssim(original, processed),
            'mse': self._mse(original, processed),
            'sharpness': self._sharpness(processed)
        }
        
        self.metrics_log.append(metrics)
        return metrics
    
    def _edge_coherence(self, img: np.ndarray) -> float:
        """Measure edge coherence (higher = more edges)."""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return np.sum(edges > 0) / edges.size
    
    def _ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate SSIM."""
        from skimage.metrics import structural_similarity
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        
        return structural_similarity(gray1, gray2)
    
    def _mse(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate MSE."""
        return np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    
    def _sharpness(self, img: np.ndarray) -> float:
        """Measure sharpness using Laplacian variance."""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        return laplacian.var()
    
    def save_metrics(self, job_id: str):
        """Save metrics to file."""
        output_file = self.output_dir / f"{job_id}_metrics.json"
        with open(output_file, 'w') as f:
            json.dump(self.metrics_log, f, indent=2)
    
    def get_summary(self) -> Dict:
        """Get summary statistics."""
        if not self.metrics_log:
            return {}
        
        return {
            'avg_processing_time': np.mean([m['processing_time'] for m in self.metrics_log]),
            'avg_edge_coherence': np.mean([m['edge_coherence'] for m in self.metrics_log]),
            'avg_ssim': np.mean([m['ssim'] for m in self.metrics_log]),
            'avg_sharpness': np.mean([m['sharpness'] for m in self.metrics_log]),
            'total_frames': len(self.metrics_log)
        }