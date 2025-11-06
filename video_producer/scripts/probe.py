"""Probe video files for metadata."""

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.io import VideoProbe


def main():
    if len(sys.argv) < 2:
        print("Usage: python probe.py <video_path>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    try:
        metadata = VideoProbe.probe(video_path)
        print(json.dumps(metadata, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()