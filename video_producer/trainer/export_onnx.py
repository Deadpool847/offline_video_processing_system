"""Export PyTorch models to ONNX."""

import torch
import onnx
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def export_to_onnx(model: torch.nn.Module,
                  output_path: str,
                  input_shape: tuple = (1, 3, 256, 256),
                  opset_version: int = 14):
    """Export PyTorch model to ONNX."""
    
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(*input_shape)
    
    try:
        # Export
        torch.onnx.export(
            model,
            dummy_input,
            output_path,
            export_params=True,
            opset_version=opset_version,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={
                'input': {0: 'batch_size', 2: 'height', 3: 'width'},
                'output': {0: 'batch_size', 2: 'height', 3: 'width'}
            }
        )
        
        # Verify
        onnx_model = onnx.load(output_path)
        onnx.checker.check_model(onnx_model)
        
        logger.info(f"Model exported successfully: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return False