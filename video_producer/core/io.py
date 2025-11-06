"""Pixel-perfect video I/O with FFmpeg and PyAV."""

import subprocess
import json
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Tuple, Iterator
import logging

# PyAV is optional - fallback to FFmpeg if not available
try:
    import av
    PYAV_AVAILABLE = True
except ImportError:
    PYAV_AVAILABLE = False
    av = None

logger = logging.getLogger(__name__)


class VideoProbe:
    """Probe video metadata with FFprobe."""
    
    @staticmethod
    def probe(video_path: str) -> Dict:
        """Extract complete video metadata."""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            # Find video and audio streams
            video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
            audio_stream = next((s for s in data['streams'] if s['codec_type'] == 'audio'), None)
            
            if not video_stream:
                raise ValueError(f"No video stream found in {video_path}")
            
            # Extract key metadata
            metadata = {
                'width': int(video_stream['width']),
                'height': int(video_stream['height']),
                'fps': eval(video_stream.get('r_frame_rate', '30/1')),
                'duration': float(data['format'].get('duration', 0)),
                'codec': video_stream['codec_name'],
                'pix_fmt': video_stream.get('pix_fmt', 'yuv420p'),
                'color_space': video_stream.get('color_space', 'unknown'),
                'color_transfer': video_stream.get('color_transfer', 'unknown'),
                'color_primaries': video_stream.get('color_primaries', 'unknown'),
                'color_range': video_stream.get('color_range', 'tv'),
                'bitrate': int(data['format'].get('bit_rate', 0)),
                'has_audio': audio_stream is not None,
                'audio_codec': audio_stream['codec_name'] if audio_stream else None,
                'audio_sample_rate': int(audio_stream.get('sample_rate', 0)) if audio_stream else None,
                'nb_frames': int(video_stream.get('nb_frames', 0)),
            }
            
            # Calculate total frames if not available
            if metadata['nb_frames'] == 0 and metadata['duration'] > 0:
                metadata['nb_frames'] = int(metadata['duration'] * metadata['fps'])
            
            return metadata
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFprobe failed: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse FFprobe output: {e}")
            raise


class VideoReader:
    """Stream-based video reader using PyAV."""
    
    def __init__(self, video_path: str, start_frame: int = 0):
        self.video_path = video_path
        self.start_frame = start_frame
        self.container = None
        self.stream = None
        self.metadata = VideoProbe.probe(video_path)
        
    def __enter__(self):
        self.container = av.open(self.video_path)
        self.stream = self.container.streams.video[0]
        
        # Seek to start frame if needed
        if self.start_frame > 0:
            timestamp = int(self.start_frame / self.metadata['fps'] * av.time_base)
            self.container.seek(timestamp)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.container:
            self.container.close()
    
    def read_frames(self, max_frames: Optional[int] = None) -> Iterator[np.ndarray]:
        """Yield frames as numpy arrays (RGB)."""
        frame_count = 0
        
        for frame in self.container.decode(video=0):
            if max_frames and frame_count >= max_frames:
                break
            
            # Convert to RGB numpy array
            img = frame.to_ndarray(format='rgb24')
            yield img
            frame_count += 1
    
    def get_metadata(self) -> Dict:
        return self.metadata


class VideoWriter:
    """Hardware-accelerated video encoder using FFmpeg."""
    
    def __init__(self, 
                 output_path: str,
                 width: int,
                 height: int,
                 fps: float,
                 codec: str = 'h264_nvenc',
                 crf: int = 18,
                 preset: str = 'p4',
                 audio_path: Optional[str] = None,
                 metadata: Optional[Dict] = None):
        
        self.output_path = output_path
        self.width = width
        self.height = height
        self.fps = fps
        self.codec = codec
        self.crf = crf
        self.preset = preset
        self.audio_path = audio_path
        self.metadata = metadata or {}
        self.process = None
        
    def __enter__(self):
        self._start_encoder()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._finish_encoder()
    
    def _start_encoder(self):
        """Start FFmpeg encoding process."""
        cmd = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{self.width}x{self.height}',
            '-pix_fmt', 'rgb24',
            '-r', str(self.fps),
            '-i', '-',  # stdin
        ]
        
        # Add audio if provided
        if self.audio_path:
            cmd.extend(['-i', self.audio_path, '-c:a', 'aac', '-b:a', '192k'])
        
        # Video encoding settings
        if 'nvenc' in self.codec:
            cmd.extend([
                '-c:v', self.codec,
                '-preset', self.preset,
                '-rc', 'vbr',
                '-cq', str(self.crf),
                '-b:v', '0',
                '-pix_fmt', 'yuv420p'
            ])
        else:
            # Fallback to libx264
            cmd.extend([
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', str(self.crf),
                '-pix_fmt', 'yuv420p'
            ])
        
        # Preserve color metadata
        if 'color_space' in self.metadata and self.metadata['color_space'] != 'unknown':
            cmd.extend(['-colorspace', self.metadata['color_space']])
        if 'color_transfer' in self.metadata and self.metadata['color_transfer'] != 'unknown':
            cmd.extend(['-color_trc', self.metadata['color_transfer']])
        if 'color_range' in self.metadata:
            cmd.extend(['-color_range', '2' if self.metadata['color_range'] == 'pc' else '1'])
        
        cmd.append(self.output_path)
        
        logger.info(f"Starting encoder: {' '.join(cmd)}")
        
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    def write_frame(self, frame: np.ndarray):
        """Write a single frame."""
        if self.process and self.process.stdin:
            self.process.stdin.write(frame.tobytes())
    
    def _finish_encoder(self):
        """Close encoder and finalize file."""
        if self.process:
            if self.process.stdin:
                self.process.stdin.close()
            self.process.wait()
            
            # Log any errors
            if self.process.stderr:
                stderr = self.process.stderr.read().decode('utf-8', errors='ignore')
                if self.process.returncode != 0:
                    logger.error(f"Encoder errors: {stderr}")
                else:
                    logger.info("Encoding completed successfully")


def check_nvenc_available() -> bool:
    """Check if NVENC is available."""
    try:
        result = subprocess.run(
            ['ffmpeg', '-hide_banner', '-encoders'],
            capture_output=True,
            text=True,
            check=True
        )
        return 'h264_nvenc' in result.stdout or 'hevc_nvenc' in result.stdout
    except:
        return False