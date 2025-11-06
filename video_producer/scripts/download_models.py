"""Download pre-trained ONNX models."""

import urllib.request
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))


def download_file(url: str, output_path: str):
    """Download file with progress."""
    print(f"Downloading: {url}")
    
    def progress_hook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\rProgress: {percent}%")
        sys.stdout.flush()
    
    try:
        urllib.request.urlretrieve(url, output_path, progress_hook)
        print(f"\nSaved to: {output_path}")
        return True
    except Exception as e:
        print(f"\nError: {e}")
        return False


def main():
    print("=" * 60)
    print("Downloading Pre-trained ONNX Models")
    print("=" * 60)
    
    assets_dir = Path(__file__).parent.parent / 'assets' / 'models'
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Model URLs (placeholder - replace with actual URLs)
    models = [
        {
            'name': 'Fast Style Transfer',
            'url': 'https://github.com/onnx/models/raw/main/vision/style_transfer/fast_neural_style/model/mosaic-9.onnx',
            'filename': 'fast_style.onnx'
        },
        # Add more models here
    ]
    
    for model in models:
        print(f"\n{model['name']}:")
        output_path = assets_dir / model['filename']
        
        if output_path.exists():
            print(f"  Already exists: {output_path}")
            continue
        
        success = download_file(model['url'], str(output_path))
        
        if not success:
            print(f"  Failed to download {model['name']}")
    
    print("\n" + "=" * 60)
    print("Download complete!")
    print(f"Models saved to: {assets_dir}")


if __name__ == '__main__':
    main()