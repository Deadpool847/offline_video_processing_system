"""Demo script - test stylizers on sample images."""

import sys
import cv2
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from stylizers import *
from core.hardware import HardwareManager


def create_sample_image():
    """Create a sample test image."""
    # Create a colorful gradient image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add gradients
    for y in range(480):
        for x in range(640):
            img[y, x, 0] = int((x / 640) * 255)  # Red gradient
            img[y, x, 1] = int((y / 480) * 255)  # Green gradient
            img[y, x, 2] = 128  # Constant blue
    
    # Add some shapes
    cv2.circle(img, (320, 240), 80, (255, 255, 0), -1)
    cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 255), -1)
    cv2.putText(img, 'TEST', (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)
    
    return img


def main():
    print("=" * 70)
    print("ML-Powered Video Producer - Stylizer Demo")
    print("=" * 70)
    
    # Hardware check
    hw_mgr = HardwareManager()
    print("\nHardware Status:")
    if hw_mgr.gpu_available:
        print(f"  ✅ GPU: {hw_mgr.gpu_info.get('name', 'Unknown')}")
    else:
        print("  ⚠️  GPU: Not detected (using CPU)")
    
    print(f"  {'NVENC:':10s} {'Available' if hw_mgr.check_nvenc() else 'Not available'}")
    
    # Create output directory
    output_dir = Path('/app/outputs/demo')
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {output_dir}")
    
    # Create sample image
    print("\nGenerating sample image...")
    img = create_sample_image()
    cv2.imwrite(str(output_dir / 'original.png'), img)
    print("  ✅ Saved: original.png")
    
    # Test stylizers
    stylizers = [
        (PencilStylizer(), 'pencil'),
        (CartoonStylizer(), 'cartoon'),
        (ComicStylizer(), 'comic'),
        (CinematicStylizer(), 'cinematic'),
    ]
    
    print("\nProcessing styles...")
    
    for stylizer, name in stylizers:
        try:
            print(f"  Processing {name}...", end=' ')
            result = stylizer.process(img)
            
            output_path = output_dir / f'{name}.png'
            cv2.imwrite(str(output_path), cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
            print(f"✅ Saved: {name}.png")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print(f"Demo complete! Check outputs in: {output_dir}")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Run Streamlit UI: streamlit run app/streamlit_app.py")
    print("  2. Or use CLI: python -m scripts.cli render --help")
    print("  3. Run benchmarks: python scripts/benchmark.py")


if __name__ == '__main__':
    main()