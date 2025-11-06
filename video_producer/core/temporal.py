"""Temporal stabilization for flicker-free video."""

import numpy as np
from typing import Optional
import cv2


class TemporalStabilizer:
    """EMA-based temporal stabilization."""
    
    def __init__(self, alpha: float = 0.3):
        """
        Args:
            alpha: EMA smoothing factor (0-1). Lower = more smoothing.
        """
        self.alpha = alpha
        self.prev_frame: Optional[np.ndarray] = None
        self.prev_edges: Optional[np.ndarray] = None
    
    def stabilize(self, frame: np.ndarray) -> np.ndarray:
        """Apply temporal smoothing."""
        if self.prev_frame is None:
            self.prev_frame = frame.copy()
            return frame
        
        # EMA blend
        stabilized = cv2.addWeighted(
            frame, self.alpha,
            self.prev_frame, 1 - self.alpha,
            0
        )
        
        self.prev_frame = stabilized.copy()
        return stabilized
    
    def stabilize_edges(self, edges: np.ndarray) -> np.ndarray:
        """Stabilize edge maps."""
        if self.prev_edges is None:
            self.prev_edges = edges.copy()
            return edges
        
        stabilized = cv2.addWeighted(
            edges, self.alpha,
            self.prev_edges, 1 - self.alpha,
            0
        )
        
        self.prev_edges = stabilized.copy()
        return stabilized
    
    def reset(self):
        """Reset stabilizer state."""
        self.prev_frame = None
        self.prev_edges = None