"""Intelligent job queue manager with background processing."""

import threading
import queue
import time
import uuid
from pathlib import Path
from typing import Dict, List, Callable, Optional
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class Job:
    """Job data structure."""
    id: str
    input_path: str
    output_path: str
    styles: List[str]
    preset: str
    status: str = 'Queued'  # Queued, Processing, Completed, Failed, Cancelled
    progress: float = 0.0
    current_frame: int = 0
    total_frames: int = 0
    fps: float = 0.0
    eta_seconds: float = 0.0
    error: Optional[str] = None
    created_at: str = ''
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    effect_intensity: float = 1.0
    
    def to_dict(self):
        return asdict(self)


class JobManager:
    """Manages job queue with background processing."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.jobs: Dict[str, Job] = {}
            self.job_queue = queue.Queue()
            self.worker_thread = None
            self.is_running = False
            self.initialized = True
            self._start_worker()
    
    def _start_worker(self):
        """Start background worker thread."""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._worker, daemon=True)
            self.worker_thread.start()
            logger.info("Job worker thread started")
    
    def _worker(self):
        """Background worker that processes jobs."""
        while self.is_running:
            try:
                job_id = self.job_queue.get(timeout=1.0)
                if job_id:
                    self._process_job(job_id)
                self.job_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")
    
    def _process_job(self, job_id: str):
        """Process a single job."""
        job = self.jobs.get(job_id)
        if not job:
            return
        
        try:
            # Update status
            job.status = 'Processing'
            job.started_at = datetime.now().isoformat()
            
            # Import here to avoid circular imports
            from .video_processor import VideoProcessor
            
            # Create processor
            processor = VideoProcessor(
                input_path=job.input_path,
                output_dir=job.output_path,
                styles=job.styles,
                preset=job.preset,
                effect_intensity=job.effect_intensity
            )
            
            # Process with progress callback
            def progress_callback(current, total, fps):
                job.current_frame = current
                job.total_frames = total
                job.progress = (current / total) * 100 if total > 0 else 0
                job.fps = fps
                
                # Calculate ETA
                if fps > 0 and total > current:
                    remaining_frames = total - current
                    job.eta_seconds = remaining_frames / fps
            
            # Process video
            result = processor.process(progress_callback=progress_callback)
            
            # Update status
            if result['success']:
                job.status = 'Completed'
                job.progress = 100.0
            else:
                job.status = 'Failed'
                job.error = result.get('error', 'Unknown error')
            
            job.completed_at = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            job.status = 'Failed'
            job.error = str(e)
            job.completed_at = datetime.now().isoformat()
    
    def add_job(self, input_path: str, output_path: str, styles: List[str], 
                preset: str, effect_intensity: float = 1.0) -> str:
        """Add job to queue."""
        job_id = str(uuid.uuid4())[:8]
        
        job = Job(
            id=job_id,
            input_path=input_path,
            output_path=output_path,
            styles=styles,
            preset=preset,
            effect_intensity=effect_intensity,
            created_at=datetime.now().isoformat()
        )
        
        self.jobs[job_id] = job
        self.job_queue.put(job_id)
        
        logger.info(f"Job {job_id} added to queue")
        return job_id
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[Job]:
        """Get all jobs."""
        return list(self.jobs.values())
    
    def cancel_job(self, job_id: str):
        """Cancel a job."""
        job = self.jobs.get(job_id)
        if job and job.status in ['Queued', 'Processing']:
            job.status = 'Cancelled'
            logger.info(f"Job {job_id} cancelled")
    
    def clear_completed(self):
        """Clear completed jobs."""
        to_remove = [jid for jid, job in self.jobs.items() 
                     if job.status in ['Completed', 'Failed', 'Cancelled']]
        for jid in to_remove:
            del self.jobs[jid]
        logger.info(f"Cleared {len(to_remove)} completed jobs")
    
    def shutdown(self):
        """Shutdown worker thread."""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)
        logger.info("Job manager shutdown")