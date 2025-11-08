"""Core video processing modules."""

from .io import VideoReader, VideoWriter
from .pipeline import Pipeline
from .temporal import TemporalStabilizer
from .color import ColorSpaceManager
from .metrics import MetricsCollector
from .ml_session import MLSession
from .autotune import AutoTuner
from .checkpoint import CheckpointManager
from .logging_config import setup_logging, get_logger
from .presets import PresetManager
from .job_manager import JobManager, Job
from .video_processor import VideoProcessor
from .pattern_learner import PatternLearner

__all__ = [
    'VideoReader',
    'VideoWriter',
    'Pipeline',
    'TemporalStabilizer',
    'ColorSpaceManager',
    'MetricsCollector',
    'MLSession',
    'AutoTuner',
    'CheckpointManager',
    'setup_logging',
    'get_logger',
    'PresetManager',
    'JobManager',
    'Job',
    'VideoProcessor',
    'PatternLearner'
]