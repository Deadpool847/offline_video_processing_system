"""Checkpoint management for resume capability."""

import json
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CheckpointManager:
    """Manage job checkpoints for resume."""
    
    def __init__(self, checkpoint_dir: str = "checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, job_id: str, state: Dict):
        """Save checkpoint state."""
        checkpoint_file = self.checkpoint_dir / f"{job_id}.json"
        
        try:
            with open(checkpoint_file, 'w') as f:
                json.dump(state, f, indent=2)
            logger.info(f"Checkpoint saved: {job_id}")
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
    
    def load(self, job_id: str) -> Optional[Dict]:
        """Load checkpoint state."""
        checkpoint_file = self.checkpoint_dir / f"{job_id}.json"
        
        if not checkpoint_file.exists():
            return None
        
        try:
            with open(checkpoint_file, 'r') as f:
                state = json.load(f)
            logger.info(f"Checkpoint loaded: {job_id}")
            return state
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None
    
    def clear(self, job_id: str):
        """Clear checkpoint."""
        checkpoint_file = self.checkpoint_dir / f"{job_id}.json"
        checkpoint_file.unlink(missing_ok=True)
        logger.info(f"Checkpoint cleared: {job_id}")
    
    def list_checkpoints(self) -> list:
        """List all checkpoints."""
        return [f.stem for f in self.checkpoint_dir.glob("*.json")]