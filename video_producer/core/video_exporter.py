"""Video export and download utilities."""

import shutil
from pathlib import Path
import logging
import zipfile
from typing import List, Optional
import subprocess

logger = logging.getLogger(__name__)


class VideoExporter:
    """Export and package processed videos."""
    
    @staticmethod
    def copy_to_location(source: str, destination: str) -> bool:
        """Copy video to destination."""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            # Create destination directory
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            logger.info(f"Copied {source_path.name} to {dest_path}")
            return True
            
        except Exception as e:
            logger.error(f"Copy failed: {e}")
            return False
    
    @staticmethod
    def create_comparison_video(original: str, processed: str, output: str) -> bool:
        """Create side-by-side comparison video."""
        try:
            cmd = [
                'ffmpeg', '-y',
                '-i', original,
                '-i', processed,
                '-filter_complex',
                '[0:v][1:v]hstack=inputs=2[v]',
                '-map', '[v]',
                '-c:v', 'libx264',
                '-crf', '23',
                '-preset', 'fast',
                output
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            logger.info(f"Created comparison video: {output}")
            return True
            
        except Exception as e:
            logger.error(f"Comparison video creation failed: {e}")
            return False
    
    @staticmethod
    def package_outputs(file_paths: List[str], output_zip: str) -> bool:
        """Package multiple videos into a zip file."""
        try:
            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in file_paths:
                    if Path(file_path).exists():
                        zipf.write(file_path, Path(file_path).name)
            
            logger.info(f"Created package: {output_zip}")
            return True
            
        except Exception as e:
            logger.error(f"Packaging failed: {e}")
            return False
    
    @staticmethod
    def get_video_info(video_path: str) -> dict:
        """Get video file information."""
        try:
            from .io import VideoProbe
            
            metadata = VideoProbe.probe(video_path)
            file_path = Path(video_path)
            
            return {
                'filename': file_path.name,
                'size_mb': file_path.stat().st_size / (1024 * 1024),
                'resolution': f"{metadata['width']}x{metadata['height']}",
                'fps': metadata['fps'],
                'duration': metadata['duration'],
                'codec': metadata['codec']
            }
            
        except Exception as e:
            logger.error(f"Failed to get video info: {e}")
            return {}
    
    @staticmethod
    def convert_format(input_path: str, output_path: str, format: str = 'mp4') -> bool:
        """Convert video to different format."""
        try:
            cmd = [
                'ffmpeg', '-y',
                '-i', input_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            logger.info(f"Converted to {format}: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Format conversion failed: {e}")
            return False