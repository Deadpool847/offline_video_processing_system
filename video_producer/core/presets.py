"""Preset management."""

import yaml
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PresetManager:
    """Manage processing presets."""
    
    DEFAULT_PRESETS = {
        'Speed': {
            'codec': 'h264_nvenc',
            'crf': 23,
            'preset': 'p1',
            'chunk_duration': 60,
            'use_temporal': False,
            'description': 'Fast processing, good quality'
        },
        'Balanced': {
            'codec': 'h264_nvenc',
            'crf': 18,
            'preset': 'p4',
            'chunk_duration': 30,
            'use_temporal': True,
            'description': 'Balanced speed and quality'
        },
        'Quality': {
            'codec': 'h264_nvenc',
            'crf': 15,
            'preset': 'p7',
            'chunk_duration': 20,
            'use_temporal': True,
            'description': 'Highest quality, slower'
        }
    }
    
    def __init__(self, preset_dir: str = "assets/presets"):
        self.preset_dir = Path(preset_dir)
        self.preset_dir.mkdir(parents=True, exist_ok=True)
        self.presets = self.DEFAULT_PRESETS.copy()
        self._load_custom_presets()
    
    def _load_custom_presets(self):
        """Load custom presets from files."""
        for preset_file in self.preset_dir.glob("*.yaml"):
            try:
                with open(preset_file, 'r') as f:
                    preset = yaml.safe_load(f)
                    preset_name = preset_file.stem
                    self.presets[preset_name] = preset
                    logger.info(f"Loaded preset: {preset_name}")
            except Exception as e:
                logger.error(f"Failed to load preset {preset_file}: {e}")
    
    def get_preset(self, name: str) -> Optional[Dict]:
        """Get preset by name."""
        return self.presets.get(name)
    
    def list_presets(self) -> list:
        """List available presets."""
        return list(self.presets.keys())
    
    def save_preset(self, name: str, preset: Dict):
        """Save custom preset."""
        preset_file = self.preset_dir / f"{name}.yaml"
        
        try:
            with open(preset_file, 'w') as f:
                yaml.dump(preset, f, default_flow_style=False)
            self.presets[name] = preset
            logger.info(f"Saved preset: {name}")
        except Exception as e:
            logger.error(f"Failed to save preset: {e}")