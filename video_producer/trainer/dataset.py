"""Dataset for style transfer training."""

import torch
from torch.utils.data import Dataset
import cv2
import numpy as np
from pathlib import Path
from typing import Tuple


class StyleDataset(Dataset):
    """Dataset for style transfer pairs."""
    
    def __init__(self, data_dir: str, transform=None):
        self.data_dir = Path(data_dir)
        self.transform = transform
        
        # Find input/target pairs
        self.pairs = self._find_pairs()
    
    def _find_pairs(self):
        """Find input/output pairs."""
        pairs = []
        
        input_dir = self.data_dir / 'input'
        target_dir = self.data_dir / 'target'
        
        if not input_dir.exists() or not target_dir.exists():
            return pairs
        
        for input_file in input_dir.glob('*.jpg'):
            target_file = target_dir / input_file.name
            if target_file.exists():
                pairs.append((str(input_file), str(target_file)))
        
        return pairs
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        input_path, target_path = self.pairs[idx]
        
        # Load images
        input_img = cv2.imread(input_path)
        target_img = cv2.imread(target_path)
        
        # Convert BGR to RGB
        input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
        target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
        
        # Apply transforms
        if self.transform:
            input_img = self.transform(input_img)
            target_img = self.transform(target_img)
        
        # Convert to tensors (NCHW)
        input_tensor = torch.from_numpy(input_img).permute(2, 0, 1).float() / 255.0
        target_tensor = torch.from_numpy(target_img).permute(2, 0, 1).float() / 255.0
        
        return input_tensor, target_tensor