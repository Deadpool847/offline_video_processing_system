"""Fast preview generator for quick video samples."""

import cv2
import numpy as np
from pathlib import Path
import logging
import tempfile
from typing import Optional, Dict, List
import subprocess
import time

from .io import VideoProbe, VideoReader, VideoWriter, check_nvenc_available
from .presets import PresetManager

logger = logging.getLogger(__name__)


class PreviewGenerator:
    """Generates quick previews from videos."""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "video_producer_previews"
        self.temp_dir.mkdir(exist_ok=True)
    
    def generate_preview(self, 
                        input_path: str,
                        stylizer,
                        duration_seconds: float = 5.0,
                        start_time: float = 0.0,
                        effect_intensity: float = 1.0) -> Dict:
        """Generate quick preview of stylized video."""
        
        try:
            # Probe video
            metadata = VideoProbe.probe(input_path)
            
            # Calculate frames
            start_frame = int(start_time * metadata['fps'])
            num_frames = int(duration_seconds * metadata['fps'])
            total_frames = metadata['nb_frames']
            
            if start_frame >= total_frames:
                start_frame = 0
            
            if start_frame + num_frames > total_frames:
                num_frames = total_frames - start_frame
            
            # Create output path
            output_name = f"preview_{Path(input_path).stem}_{int(time.time())}.mp4"
            output_path = self.temp_dir / output_name
            
            # Determine codec
            codec = 'h264_nvenc' if check_nvenc_available() else 'libx264'
            
            # Process frames
            frame_count = 0
            start_process = time.time()
            
            with VideoReader(input_path, start_frame=start_frame) as reader:
                with VideoWriter(
                    str(output_path),
                    metadata['width'],
                    metadata['height'],
                    metadata['fps'],
                    codec=codec,
                    crf=23,  # Fast encoding
                    metadata=metadata
                ) as writer:
                    
                    for frame in reader.read_frames(max_frames=num_frames):
                        # Apply style with intensity
                        processed = stylizer.process(frame)
                        
                        # Scale effect intensity
                        if effect_intensity != 1.0:
                            processed = self._blend_frames(frame, processed, effect_intensity)
                        
                        writer.write_frame(processed)
                        frame_count += 1
            
            processing_time = time.time() - start_process
            avg_fps = frame_count / processing_time if processing_time > 0 else 0
            
            return {
                'success': True,
                'output_path': str(output_path),
                'frames_processed': frame_count,
                'processing_time': processing_time,
                'avg_fps': avg_fps,
                'duration': duration_seconds
            }
            
        except Exception as e:
            logger.error(f"Preview generation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _blend_frames(self, original: np.ndarray, processed: np.ndarray, 
                     intensity: float) -> np.ndarray:
        """Blend original and processed frames based on intensity."""
        if intensity >= 1.0:
            return processed
        
        # Linear blend
        blended = cv2.addWeighted(
            original, 1.0 - intensity,
            processed, intensity,
            0
        )
        return blended
    
    def extract_thumbnail(self, video_path: str, time_seconds: float = 1.0) -> Optional[str]:
        """Extract a thumbnail from video."""
        try:
            output_path = self.temp_dir / f"thumb_{Path(video_path).stem}_{int(time.time())}.jpg"
            
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(time_seconds),
                '-i', video_path,
                '-vframes', '1',
                '-q:v', '2',
                str(output_path)
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Thumbnail extraction failed: {e}")
            return None
    
    def cleanup_old_previews(self, max_age_hours: int = 24):
        """Clean up old preview files."""
        import time as time_module
        
        current_time = time_module.time()
        max_age_seconds = max_age_hours * 3600
        
        for file in self.temp_dir.glob('*'):
            if file.is_file():
                age = current_time - file.stat().st_mtime
                if age > max_age_seconds:
                    try:
                        file.unlink()
                        logger.info(f"Cleaned up old preview: {file.name}")
                    except Exception as e:
                        logger.error(f"Failed to clean up {file}: {e}")