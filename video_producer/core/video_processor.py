"""Intelligent video processor with pattern learning."""

import numpy as np
import cv2
from pathlib import Path
from typing import List, Callable, Optional, Dict
import logging
import time

from .io import VideoProbe, VideoReader, VideoWriter, check_nvenc_available
from .presets import PresetManager
from .pattern_learner import PatternLearner
from .color import ColorSpaceManager

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Processes videos with intelligent parameter optimization."""
    
    def __init__(self, input_path: str, output_dir: str, styles: List[str],
                 preset: str = 'Balanced', effect_intensity: float = 1.0):
        self.input_path = input_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = styles
        self.preset_name = preset
        self.effect_intensity = effect_intensity
        
        # Load preset
        preset_mgr = PresetManager()
        self.preset = preset_mgr.get_preset(preset)
        
        # Probe video
        self.metadata = VideoProbe.probe(input_path)
        
        # Pattern learner for intelligent optimization
        self.learner = PatternLearner()
        
        # Analyze video and optimize parameters
        self._analyze_and_optimize()
    
    def _analyze_and_optimize(self):
        """Analyze video and optimize parameters using pattern learning."""
        logger.info("Analyzing video characteristics...")
        
        # Sample frames from video
        sample_frames = self._extract_sample_frames(num_samples=10)
        
        # Analyze characteristics
        characteristics = self.learner.analyze_video(sample_frames)
        
        # Get optimized parameters
        self.optimized_params = self.learner.get_optimized_params(
            characteristics, 
            self.styles
        )
        
        logger.info(f"Video analysis complete: {characteristics}")
        logger.info(f"Optimized parameters: {self.optimized_params}")
    
    def _extract_sample_frames(self, num_samples: int = 10) -> List[np.ndarray]:
        """Extract sample frames for analysis."""
        frames = []
        total_frames = self.metadata['nb_frames']
        
        if total_frames == 0:
            return frames
        
        # Sample evenly throughout video
        sample_indices = np.linspace(0, total_frames - 1, num_samples, dtype=int)
        
        try:
            with VideoReader(self.input_path) as reader:
                for i, frame in enumerate(reader.read_frames()):
                    if i in sample_indices:
                        frames.append(frame)
                    if len(frames) >= num_samples:
                        break
        except Exception as e:
            logger.warning(f"Failed to extract samples: {e}")
        
        return frames
    
    def process(self, progress_callback: Optional[Callable] = None) -> Dict:
        """Process video with all selected styles."""
        results = {'success': True, 'outputs': [], 'errors': []}
        
        for style in self.styles:
            try:
                output_path = self.output_dir / f"{Path(self.input_path).stem}_{style.lower().replace(' ', '_')}.mp4"
                
                logger.info(f"Processing style: {style}")
                
                # Get stylizer
                stylizer = self._get_stylizer(style)
                
                # Process video
                self._process_single_style(
                    stylizer=stylizer,
                    style_name=style,
                    output_path=str(output_path),
                    progress_callback=progress_callback
                )
                
                results['outputs'].append(str(output_path))
                
            except Exception as e:
                logger.error(f"Failed to process style {style}: {e}")
                results['errors'].append(f"{style}: {str(e)}")
                results['success'] = False
        
        return results
    
    def _get_stylizer(self, style: str):
        """Get stylizer instance with optimized parameters."""
        from stylizers import (PencilStylizer, CartoonStylizer, ComicStylizer,
                              CinematicStylizer, FastStyleStylizer)
        
        # Get optimized params for this style
        params = self.optimized_params.get(style, {})
        
        # Apply intensity scaling
        params = self._scale_params(params, self.effect_intensity)
        
        if 'Pencil' in style:
            return PencilStylizer(**params)
        elif 'Cartoon' in style:
            return CartoonStylizer(**params)
        elif 'Comic' in style:
            return ComicStylizer(**params)
        elif 'Cinematic' in style:
            return CinematicStylizer(**params)
        elif 'Neural' in style or 'Fast' in style:
            return FastStyleStylizer(model_path='assets/models/fast_style.onnx')
        else:
            return PencilStylizer()
    
    def _scale_params(self, params: Dict, intensity: float) -> Dict:
        """Scale effect parameters by intensity."""
        scaled = params.copy()
        
        # Scale numeric parameters
        for key, value in params.items():
            if isinstance(value, (int, float)):
                if key in ['blur_sigma', 'bilateral_sigma_color', 'bilateral_sigma_space']:
                    # Larger values = more effect
                    scaled[key] = value * intensity
                elif key in ['num_colors']:
                    # Inverse: fewer colors = more effect
                    original = 16  # max colors
                    scaled[key] = int(original - (original - value) * intensity)
                elif key in ['bloom_strength', 'grain_strength', 'vignette_strength']:
                    # Direct scaling
                    scaled[key] = value * intensity
        
        return scaled
    
    def _process_single_style(self, stylizer, style_name: str, output_path: str,
                              progress_callback: Optional[Callable] = None):
        """Process video with single style."""
        # Determine codec
        codec = self.preset.get('codec', 'libx264')
        if codec == 'h264_nvenc' and not check_nvenc_available():
            codec = 'libx264'
            logger.warning("NVENC not available, falling back to libx264")
        
        # Process video
        frame_count = 0
        start_time = time.time()
        
        with VideoReader(self.input_path) as reader:
            with VideoWriter(
                output_path,
                self.metadata['width'],
                self.metadata['height'],
                self.metadata['fps'],
                codec=codec,
                crf=self.preset.get('crf', 18),
                metadata=self.metadata
            ) as writer:
                
                for frame in reader.read_frames():
                    # Apply style
                    processed = stylizer.process(frame)
                    
                    # Write frame
                    writer.write_frame(processed)
                    
                    frame_count += 1
                    
                    # Update progress
                    if progress_callback and frame_count % 10 == 0:
                        elapsed = time.time() - start_time
                        fps = frame_count / elapsed if elapsed > 0 else 0
                        progress_callback(
                            frame_count,
                            self.metadata['nb_frames'],
                            fps
                        )
        
        logger.info(f"Completed {style_name}: {output_path}")