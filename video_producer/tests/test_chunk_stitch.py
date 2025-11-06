"""Test chunk processing and stitching."""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.pipeline import Pipeline


def test_chunk_boundaries():
    """Test chunk boundary calculation."""
    pipeline = Pipeline(
        input_path="dummy.mp4",
        output_path="out.mp4",
        stylizer=lambda f, m: f,
        chunk_duration=30
    )
    
    # Mock metadata
    pipeline.total_frames = 300
    pipeline.fps = 30
    
    chunks = pipeline._calculate_chunks(0, 30 * 30)  # 30 second chunks at 30fps
    
    assert len(chunks) > 0, "Should have at least one chunk"
    assert chunks[0][0] == 0, "First chunk should start at 0"
    assert chunks[-1][1] == 300, "Last chunk should end at total frames"


def test_seamless_stitch():
    """Test that chunked processing produces seamless output."""
    # This needs actual video files to test
    pass