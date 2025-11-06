"""Async chunked video processing pipeline."""

import asyncio
import numpy as np
from pathlib import Path
from typing import Callable, Dict, Optional, List, Tuple
from queue import Queue
from threading import Thread
import logging

from .io import VideoReader, VideoWriter, VideoProbe
from .checkpoint import CheckpointManager
from .temporal import TemporalStabilizer

logger = logging.getLogger(__name__)


class Pipeline:
    """Chunked video processing pipeline with resume capability."""
    
    def __init__(self,
                 input_path: str,
                 output_path: str,
                 stylizer: Callable[[np.ndarray, Dict], np.ndarray],
                 chunk_duration: int = 30,
                 max_queue_size: int = 60,
                 use_temporal: bool = True,
                 checkpoint_dir: Optional[str] = None):
        
        self.input_path = input_path
        self.output_path = output_path
        self.stylizer = stylizer
        self.chunk_duration = chunk_duration
        self.max_queue_size = max_queue_size
        self.use_temporal = use_temporal
        
        # Metadata
        self.metadata = VideoProbe.probe(input_path)
        self.total_frames = self.metadata['nb_frames']
        self.fps = self.metadata['fps']
        
        # Checkpoint management
        if checkpoint_dir:
            self.checkpoint_mgr = CheckpointManager(checkpoint_dir)
            self.job_id = Path(input_path).stem
        else:
            self.checkpoint_mgr = None
            self.job_id = None
        
        # Temporal stabilizer
        self.temporal_stabilizer = TemporalStabilizer() if use_temporal else None
        
        # Processing state
        self.frames_processed = 0
        self.is_cancelled = False
        
    def process(self, 
                progress_callback: Optional[Callable[[int, int], None]] = None,
                codec: str = 'h264_nvenc',
                crf: int = 18) -> Dict:
        """Process video with chunking and resume capability."""
        
        # Check for existing checkpoint
        start_frame = 0
        if self.checkpoint_mgr and self.job_id:
            checkpoint = self.checkpoint_mgr.load(self.job_id)
            if checkpoint:
                start_frame = checkpoint.get('last_frame', 0)
                logger.info(f"Resuming from frame {start_frame}")
        
        # Calculate chunks
        chunk_frames = int(self.chunk_duration * self.fps)
        chunks = self._calculate_chunks(start_frame, chunk_frames)
        
        logger.info(f"Processing {len(chunks)} chunks, total {self.total_frames} frames")
        
        # Process chunks
        chunk_outputs = []
        
        for i, (chunk_start, chunk_end) in enumerate(chunks):
            if self.is_cancelled:
                logger.warning("Processing cancelled")
                break
            
            logger.info(f"Processing chunk {i+1}/{len(chunks)}: frames {chunk_start}-{chunk_end}")
            
            chunk_output = self._process_chunk(
                chunk_start, 
                chunk_end,
                codec=codec,
                crf=crf
            )
            
            chunk_outputs.append(chunk_output)
            
            # Update progress
            self.frames_processed = chunk_end
            if progress_callback:
                progress_callback(self.frames_processed, self.total_frames)
            
            # Save checkpoint
            if self.checkpoint_mgr and self.job_id:
                self.checkpoint_mgr.save(self.job_id, {
                    'last_frame': chunk_end,
                    'total_frames': self.total_frames,
                    'chunks_completed': i + 1,
                    'codec': codec,
                    'crf': crf
                })
        
        # Stitch chunks if multiple
        if len(chunk_outputs) > 1:
            logger.info("Stitching chunks...")
            self._stitch_chunks(chunk_outputs, self.output_path)
            # Clean up chunk files
            for chunk_file in chunk_outputs:
                Path(chunk_file).unlink(missing_ok=True)
        elif len(chunk_outputs) == 1:
            # Single chunk, just rename
            Path(chunk_outputs[0]).rename(self.output_path)
        
        # Clear checkpoint on success
        if self.checkpoint_mgr and self.job_id and not self.is_cancelled:
            self.checkpoint_mgr.clear(self.job_id)
        
        return {
            'output_path': self.output_path,
            'frames_processed': self.frames_processed,
            'chunks': len(chunks),
            'success': not self.is_cancelled
        }
    
    def _calculate_chunks(self, start_frame: int, chunk_frames: int) -> List[Tuple[int, int]]:
        """Calculate chunk boundaries."""
        chunks = []
        current = start_frame
        
        while current < self.total_frames:
            end = min(current + chunk_frames, self.total_frames)
            chunks.append((current, end))
            current = end
        
        return chunks
    
    def _process_chunk(self, start_frame: int, end_frame: int, codec: str, crf: int) -> str:
        """Process a single chunk."""
        # Create temporary chunk file
        chunk_output = f"{self.output_path}.chunk_{start_frame}_{end_frame}.mp4"
        
        num_frames = end_frame - start_frame
        
        # Read and process frames
        with VideoReader(self.input_path, start_frame=start_frame) as reader:
            with VideoWriter(
                chunk_output,
                self.metadata['width'],
                self.metadata['height'],
                self.fps,
                codec=codec,
                crf=crf,
                metadata=self.metadata
            ) as writer:
                
                for frame in reader.read_frames(max_frames=num_frames):
                    # Apply stylizer
                    processed = self.stylizer(frame, self.metadata)
                    
                    # Apply temporal stabilization
                    if self.temporal_stabilizer:
                        processed = self.temporal_stabilizer.stabilize(processed)
                    
                    # Write frame
                    writer.write_frame(processed)
        
        return chunk_output
    
    def _stitch_chunks(self, chunk_files: List[str], output_path: str):
        """Stitch chunks using FFmpeg concat."""
        import subprocess
        import tempfile
        
        # Create concat file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            for chunk in chunk_files:
                f.write(f"file '{chunk}'\n")
            concat_file = f.name
        
        try:
            # Concat with stream copy (lossless)
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file,
                '-c', 'copy',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Successfully stitched {len(chunk_files)} chunks")
            
        finally:
            Path(concat_file).unlink(missing_ok=True)
    
    def cancel(self):
        """Cancel processing."""
        self.is_cancelled = True