"""Fine-tuning for style transfer models."""

import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class FineTuner:
    """Fine-tune style transfer models."""
    
    def __init__(self, 
                 model: nn.Module,
                 device: str = 'cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = model.to(device)
        self.device = device
        self.best_loss = float('inf')
        self.best_state = None
    
    def train_epoch(self,
                   dataloader,
                   optimizer,
                   criterion,
                   epoch: int) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        
        for batch_idx, (inputs, targets) in enumerate(dataloader):
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = criterion(outputs, targets)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 10 == 0:
                logger.info(f"Epoch {epoch} [{batch_idx}/{len(dataloader)}] Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(dataloader)
        return avg_loss
    
    def validate(self, dataloader, criterion) -> float:
        """Validate model."""
        self.model.eval()
        total_loss = 0.0
        
        with torch.no_grad():
            for inputs, targets in dataloader:
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                
                outputs = self.model(inputs)
                loss = criterion(outputs, targets)
                total_loss += loss.item()
        
        avg_loss = total_loss / len(dataloader)
        return avg_loss
    
    def train(self,
             train_loader,
             val_loader,
             epochs: int = 1,
             lr: float = 0.001,
             save_path: Optional[str] = None) -> Dict:
        """Full training loop."""
        
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.MSELoss()
        
        history = {'train_loss': [], 'val_loss': []}
        
        for epoch in range(1, epochs + 1):
            logger.info(f"Epoch {epoch}/{epochs}")
            
            # Train
            train_loss = self.train_epoch(train_loader, optimizer, criterion, epoch)
            history['train_loss'].append(train_loss)
            
            # Validate
            val_loss = self.validate(val_loader, criterion)
            history['val_loss'].append(val_loss)
            
            logger.info(f"Epoch {epoch} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
            
            # Save best model
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                self.best_state = self.model.state_dict().copy()
                logger.info(f"New best model (loss: {val_loss:.4f})")
                
                if save_path:
                    torch.save(self.best_state, save_path)
        
        # Restore best model
        if self.best_state:
            self.model.load_state_dict(self.best_state)
        
        return history
    
    def save_checkpoint(self, path: str):
        """Save model checkpoint."""
        torch.save({
            'model_state': self.model.state_dict(),
            'best_loss': self.best_loss
        }, path)
        logger.info(f"Checkpoint saved: {path}")
    
    def load_checkpoint(self, path: str):
        """Load model checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state'])
        self.best_loss = checkpoint.get('best_loss', float('inf'))
        logger.info(f"Checkpoint loaded: {path}")