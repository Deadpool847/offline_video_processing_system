"""Benchmark processing performance."""

import sys
import time
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from stylizers import *
from core.hardware import HardwareManager


def benchmark_stylizer(stylizer, name, frame, iterations=100):
    """Benchmark a stylizer."""
    print(f"\nBenchmarking {name}...")
    
    times = []
    
    for i in range(iterations):
        start = time.time()
        result = stylizer.process(frame)
        elapsed = time.time() - start
        times.append(elapsed)
    
    avg_time = np.mean(times)
    fps = 1.0 / avg_time
    
    print(f"  Average time: {avg_time*1000:.2f} ms")
    print(f"  FPS: {fps:.2f}")
    
    return {'name': name, 'avg_time': avg_time, 'fps': fps}


def main():
    print("=" * 60)
    print("ML-Powered Video Producer - Benchmark")
    print("=" * 60)
    
    # Hardware info
    hw_mgr = HardwareManager()
    
    print("\nHardware:")
    if hw_mgr.gpu_available:
        print(f"  GPU: {hw_mgr.gpu_info.get('name', 'Unknown')}")
        print(f"  Driver: {hw_mgr.gpu_info.get('driver_version', 'Unknown')}")
        print(f"  NVENC: {'Yes' if hw_mgr.check_nvenc() else 'No'}")
    else:
        print("  GPU: Not detected (CPU mode)")
    
    # Create test frame (1080p)
    frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    print(f"\nTest frame: {frame.shape} ({frame.dtype})")
    
    # Benchmark stylizers
    results = []
    
    stylizers = [
        (PencilStylizer(), 'Pencil Sketch'),
        (CartoonStylizer(), 'Cartoon'),
        (ComicStylizer(), 'Comic/Halftone'),
        (CinematicStylizer(), 'Cinematic'),
    ]
    
    for stylizer, name in stylizers:
        result = benchmark_stylizer(stylizer, name, frame, iterations=50)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    for result in sorted(results, key=lambda x: x['fps'], reverse=True):
        print(f"{result['name']:20s} - {result['fps']:6.2f} fps")
    
    print("\nNote: Actual performance depends on video content and hardware.")


if __name__ == '__main__':
    main()