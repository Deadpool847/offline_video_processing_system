"""Auto-parameter tuning for styles."""

import numpy as np
from typing import Dict, Callable, List, Tuple
import logging

logger = logging.getLogger(__name__)


class AutoTuner:
    """Auto-tune style parameters."""
    
    def __init__(self):
        self.best_params = {}
    
    def tune_parameters(self,
                       sample_frame: np.ndarray,
                       stylizer: Callable,
                       param_ranges: Dict[str, List],
                       metric: str = 'edge_coherence') -> Dict:
        """Search parameter space for best results."""
        
        logger.info(f"Tuning parameters for {len(param_ranges)} params")
        
        best_score = -np.inf
        best_params = {}
        
        # Grid search (simplified for MVP)
        for param_name, param_values in param_ranges.items():
            for value in param_values:
                # Create param dict
                test_params = {param_name: value}
                
                # Apply stylizer
                try:
                    result = stylizer(sample_frame, test_params)
                    score = self._evaluate_result(result, metric)
                    
                    if score > best_score:
                        best_score = score
                        best_params[param_name] = value
                        
                except Exception as e:
                    logger.warning(f"Failed to test {param_name}={value}: {e}")
        
        logger.info(f"Best params: {best_params} (score: {best_score:.4f})")
        self.best_params = best_params
        
        return best_params
    
    def _evaluate_result(self, img: np.ndarray, metric: str) -> float:
        """Evaluate stylized result."""
        import cv2
        
        if metric == 'edge_coherence':
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            return np.sum(edges > 0) / edges.size
        
        elif metric == 'sharpness':
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            return laplacian.var()
        
        else:
            return 0.0